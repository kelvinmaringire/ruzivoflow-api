import pandas as pd
import io
from django.core.files.base import ContentFile
from wagtail.documents.models import Document
from wagtail.models import Collection
from node_editor.models import NodeItem


VALID_FORMATS = {'json', 'csv', 'excel'}
EXTENSIONS = {'json': '.json', 'csv': '.csv', 'excel': '.xlsx'}


def init_save_file_from_parent(node_item):
    """
    On connection created: copy parent's parquet to this node and set response_data
    with column names and HTML table preview. Called when target is a save_file node.
    """
    if not node_item.parent:
        return {
            'html_table': '',
            'stats': {'rows': 0, 'columns': 0, 'column_names': []},
            'file_id': None,
            'message': 'No parent connected.',
        }

    parent_response = node_item.parent.response_data or {}
    parquet_file_id = parent_response.get('parquet_file_id')

    if parquet_file_id is None:
        return {
            'html_table': '',
            'stats': {'rows': 0, 'columns': 0, 'column_names': []},
            'file_id': None,
            'message': 'Run the parent node first.',
        }

    try:
        parquet_doc = Document.objects.get(id=parquet_file_id)
    except Document.DoesNotExist:
        return {
            'html_table': '',
            'stats': {'rows': 0, 'columns': 0, 'column_names': []},
            'file_id': None,
            'message': 'Parent parquet document not found.',
        }

    with parquet_doc.file.open(mode='rb') as f:
        df = pd.read_parquet(f)

    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
    parquet_buffer.seek(0)

    collection, _ = Collection.objects.get_or_create(name='Parquet')
    parquet_filename = f'{node_item.html_id}.parquet'

    existing_doc = Document.objects.filter(
        title=node_item.html_id,
        collection=collection
    ).first()

    parquet_file = ContentFile(parquet_buffer.read(), name=parquet_filename)

    if existing_doc:
        existing_doc.file.save(parquet_filename, parquet_file, save=True)
        parquet_doc = existing_doc
    else:
        parquet_doc = Document.objects.create(
            title=node_item.html_id,
            file=parquet_file,
            collection=collection
        )

    return {
        'html_table': df.head().to_html(index=False),
        'stats': {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns)
        },
        'parquet_file_id': parquet_doc.id,
        'parquet_file_url': parquet_doc.file.url,
        'parquet_file_title': parquet_doc.title,
        'file_id': None,
    }


def save_file(form_data):
    """
    Read from this node's own parquet file (or parent's if not yet initialized),
    convert to JSON/CSV/Excel (format from frontend), save to collection_id=4.
    One file per node (replace when format changes).
    """
    try:
        node_item_id = form_data.get('node_item_id')
        format_key = form_data.get('format', '').lower().strip()

        if format_key not in VALID_FORMATS:
            raise ValueError(
                f'Invalid format "{format_key}". Choose json, csv, or excel.'
            )

        node_item = NodeItem.objects.get(id=node_item_id)

        # Prefer own parquet (from init on connection), then parent's
        parquet_file_id = None
        if node_item.response_data:
            parquet_file_id = node_item.response_data.get('parquet_file_id')
        if parquet_file_id is None and node_item.parent:
            parent_response = node_item.parent.response_data or {}
            parquet_file_id = parent_response.get('parquet_file_id')
        if parquet_file_id is None:
            raise ValueError(
                'No input data. Connect this node to a data source and run the parent node first.'
            )

        parquet_doc = Document.objects.get(id=parquet_file_id)
        with parquet_doc.file.open(mode='rb') as f:
            df = pd.read_parquet(f)

        ext = EXTENSIONS[format_key]
        filename = f'{node_item.html_id}{ext}'

        if format_key == 'json':
            content_str = df.to_json(orient='records')
            file_content = ContentFile(content_str.encode('utf-8'), name=filename)
        elif format_key == 'csv':
            content_str = df.to_csv(index=False)
            file_content = ContentFile(content_str.encode('utf-8'), name=filename)
        else:  # excel
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            file_content = ContentFile(buffer.read(), name=filename)

        collection = Collection.objects.get(id=4)
        existing_doc = Document.objects.filter(
            title=node_item.html_id,
            collection=collection
        ).first()

        if existing_doc:
            existing_doc.file.save(filename, file_content, save=True)
            document = existing_doc
        else:
            document = Document.objects.create(
                title=node_item.html_id,
                file=file_content,
                collection=collection
            )

        return {
            'html_table': df.head().to_html(index=False),
            'stats': {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns)
            },
            'file_id': document.id,
            'file_url': document.file.url,
            'file_title': document.title
        }

    except Document.DoesNotExist:
        raise ValueError(f'Document with id {parquet_file_id} does not exist.')
    except NodeItem.DoesNotExist:
        raise ValueError(f'NodeItem with id {node_item_id} does not exist.')
    except Collection.DoesNotExist:
        raise ValueError('Collection with id 4 does not exist.')
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise RuntimeError(f'An error occurred: {e}')
