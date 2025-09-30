import pandas as pd
import json
import io
from django.core.files.base import ContentFile
from wagtail.documents.models import Document
from wagtail.models import Collection
from node_editor.models import NodeItem


def read_json(form_data):
    try:
        # 1. Get the original Wagtail document
        document_id = form_data.get("file_id")
        original_doc = Document.objects.get(id=document_id)

        # 2. Load JSON content
        with original_doc.file.open(mode='r') as f:
            json_data = json.load(f)

        # 3. Convert to DataFrame
        df = pd.DataFrame(json_data)

        # 4. Convert DataFrame to in-memory Parquet
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
        parquet_buffer.seek(0)

        # 5. Get or create "Parquet" collection
        collection, _ = Collection.objects.get_or_create(name="Parquet")

        # 6. Get NodeItem
        node_item_id = form_data.get("node_item_id")
        node_item = NodeItem.objects.get(id=node_item_id)
        parquet_filename = f"{node_item.html_id}.parquet"

        # 7. Check if a Document with this node already exists
        existing_doc = Document.objects.filter(
            title=node_item.html_id,
            collection=collection
        ).first()

        # 8. Create a Django file from the Parquet buffer
        parquet_file = ContentFile(parquet_buffer.read(), name=parquet_filename)

        if existing_doc:
            # Update existing document (replace file)
            existing_doc.file.save(parquet_filename, parquet_file, save=True)
            parquet_doc = existing_doc
        else:
            # Create new document
            parquet_doc = Document.objects.create(
                title=node_item.html_id,
                file=parquet_file,
                collection=collection
            )

        # 9. Return DataFrame preview and document info
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

    except Document.DoesNotExist:
        raise ValueError(f"Document with id {document_id} does not exist.")
    except NodeItem.DoesNotExist:
        raise ValueError(f"NodeItem with id {node_item_id} does not exist.")
    except json.JSONDecodeError:
        raise ValueError("The file is not a valid JSON.")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")
