import pandas as pd
import io
from django.core.files.base import ContentFile
from wagtail.documents.models import Document
from wagtail.models import Collection
from node_editor.models import NodeItem


def init_select_columns_from_parent(node_item):
    """
    On connection created: copy parent's parquet to this node and set response_data
    with column names and HTML table preview. Called when target is a select_columns node.
    """
    if not node_item.parent:
        return {
            'html_table': '',
            'stats': {'rows': 0, 'columns': 0, 'column_names': []},
            'message': 'No parent connected.',
        }

    parent_response = node_item.parent.response_data or {}
    parquet_file_id = parent_response.get('parquet_file_id')

    if parquet_file_id is None:
        return {
            'html_table': '',
            'stats': {'rows': 0, 'columns': 0, 'column_names': []},
            'message': 'Run the parent node first.',
        }

    try:
        parquet_doc = Document.objects.get(id=parquet_file_id)
    except Document.DoesNotExist:
        return {
            'html_table': '',
            'stats': {'rows': 0, 'columns': 0, 'column_names': []},
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
        'parquet_file_title': parquet_doc.title
    }


def select_columns(form_data):
    """
    Always read from the parent's parquet file, select columns, and write the
    result to this node's own parquet (updating this node's Document).
    """
    try:
        node_item_id = form_data.get('node_item_id')
        node_item = NodeItem.objects.get(id=node_item_id)

        # Always use parent's parquet as source
        if not node_item.parent:
            raise ValueError(
                'No input data. Connect this node to a data source (e.g. Read CSV, Read JSON) first.'
            )
        parent_response = node_item.parent.response_data or {}
        parquet_file_id = parent_response.get('parquet_file_id')
        if parquet_file_id is None:
            raise ValueError(
                'No input data. Run the parent node first.'
            )

        parquet_doc = Document.objects.get(id=parquet_file_id)
        with parquet_doc.file.open(mode='rb') as f:
            df = pd.read_parquet(f)

        selected_columns = form_data.get('selected_columns') or form_data.get('columns') or []
        if not selected_columns:
            raise ValueError('No columns selected. Please select at least one column.')

        missing = [c for c in selected_columns if c not in df.columns]
        if missing:
            raise ValueError(f'Columns not found in data: {missing}')

        df_selected = df[selected_columns].copy()

        parquet_buffer = io.BytesIO()
        df_selected.to_parquet(parquet_buffer, index=False, engine='pyarrow')
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
            'html_table': df_selected.head().to_html(index=False),
            'stats': {
                'rows': len(df_selected),
                'columns': len(df_selected.columns),
                'column_names': list(df_selected.columns)
            },
            'parquet_file_id': parquet_doc.id,
            'parquet_file_url': parquet_doc.file.url,
            'parquet_file_title': parquet_doc.title
        }

    except Document.DoesNotExist:
        raise ValueError(f'Parquet document with id {parquet_file_id} does not exist.')
    except NodeItem.DoesNotExist:
        raise ValueError(f'NodeItem with id {node_item_id} does not exist.')
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise RuntimeError(f'An error occurred: {e}')
