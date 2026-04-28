"""
Python Code node: executes user Python code with input_df from upstream data.
Returns response_data with html_table, stats, parquet for pipeline compatibility.
"""
import io
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.core.files.base import ContentFile
from wagtail.documents.models import Document
from wagtail.models import Collection

from node_editor.models import NodeItem

DEFAULT_TIMEOUT = 60
RUNNER_SCRIPT = """
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]
code_path = sys.argv[3]

import pandas as pd

with open(code_path, 'r', encoding='utf-8') as f:
    code = f.read()

input_df = pd.read_parquet(input_path)

globs = {
    'input_df': input_df,
    'pd': pd,
    'pandas': pd,
}
exec(code, globs)

output_df = globs.get('output_df')
if output_df is None:
    raise NameError("output_df must be defined by your code")
if not isinstance(output_df, pd.DataFrame):
    raise TypeError("output_df must be a pandas DataFrame")
output_df.to_parquet(output_path, index=False, engine='pyarrow')
"""


def _error_response(error_msg, stdout='', stderr='', execution_time_ms=0):
    """Build error response_data dict (no raise)."""
    execution_log = stdout
    if stderr:
        execution_log = f"{execution_log}\n[stderr]\n{stderr}".strip() if execution_log else f"[stderr]\n{stderr}"
    return {
        'stdout': stdout,
        'stderr': stderr,
        'error': error_msg,
        'execution_log': execution_log or error_msg,
        'execution_time_ms': execution_time_ms,
        'status': 'error',
    }


def _load_input_dataframe(form_data):
    """
    Resolve input DataFrame from parent's parquet (like select_columns/save_file),
    then input_data.parquet_file_id, then html_table fallback.
    Returns (df, error_response) - if error_response is not None, df is None.
    """
    input_data = form_data.get('input_data') or {}
    node_item_id = form_data.get('node_item_id')
    node_item = NodeItem.objects.get(id=node_item_id)

    # Prefer parent's parquet first (same as select_columns, save_file)
    parquet_file_id = None
    if node_item.parent:
        parent_response = node_item.parent.response_data or {}
        parquet_file_id = parent_response.get('parquet_file_id')
    if parquet_file_id is None:
        parquet_file_id = input_data.get('parquet_file_id')

    if parquet_file_id is not None:
        try:
            parquet_doc = Document.objects.get(id=parquet_file_id)
            with parquet_doc.file.open(mode='rb') as f:
                return pd.read_parquet(f), None
        except Document.DoesNotExist:
            return None, _error_response(
                f'Parquet document with id {parquet_file_id} does not exist.'
            )

    html_table = input_data.get('html_table', '')
    if html_table:
        try:
            dfs = pd.read_html(io.StringIO(html_table))
            if dfs:
                return dfs[0], None
        except Exception as e:
            return None, _error_response(f'Failed to parse html_table: {e}')

    if not node_item.parent:
        return None, _error_response(
            'No input data. Connect this node to a data source (e.g. Read CSV, Read JSON, Select Columns) and run it first.'
        )
    return None, _error_response(
        'No input data. Run the parent node first.'
    )


def _persist_parquet(node_item, output_df):
    """Persist output_df to Wagtail Parquet collection (same pattern as read_csv)."""
    parquet_buffer = io.BytesIO()
    output_df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
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

    return parquet_doc


def python_code(form_data):
    """
    Execute user Python code with input_df from upstream data.
    - Save only (no input_data): return {} so response_data is not overwritten.
    - Run (with input_data): load input_df, execute code, return success or error payload.
    """
    input_data = form_data.get('input_data')
    if not input_data:
        return {}

    code = form_data.get('code', '')
    if not code or not code.strip():
        return _error_response('No code provided.')

    node_item_id = form_data.get('node_item_id')
    if node_item_id is None:
        return _error_response('node_item_id is required.')

    try:
        node_item = NodeItem.objects.get(id=node_item_id)
    except NodeItem.DoesNotExist:
        return _error_response(f'NodeItem with id {node_item_id} does not exist.')

    input_df, err = _load_input_dataframe(form_data)
    if err is not None:
        return err

    timeout_seconds = getattr(
        settings, 'PYTHON_NODE_TIMEOUT_SECONDS', DEFAULT_TIMEOUT
    )

    start = time.perf_counter()
    stdout = ''
    stderr = ''

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        input_path = tmp / 'input.parquet'
        output_path = tmp / 'output.parquet'
        code_path = tmp / 'code.py'
        runner_path = tmp / 'runner.py'

        try:
            input_df.to_parquet(input_path, index=False, engine='pyarrow')
            code_path.write_text(code, encoding='utf-8')
            runner_path.write_text(RUNNER_SCRIPT, encoding='utf-8')

            result = subprocess.run(
                [sys.executable, str(runner_path), str(input_path), str(output_path), str(code_path)],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=str(tmp),
            )
            stdout = result.stdout or ''
            stderr = result.stderr or ''
        except subprocess.TimeoutExpired as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return _error_response(
                f'Execution timed out after {timeout_seconds} seconds.',
                stdout=getattr(e, 'stdout', '') or '',
                stderr=getattr(e, 'stderr', '') or '',
                execution_time_ms=elapsed_ms,
            )
        except Exception as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return _error_response(str(e), execution_time_ms=elapsed_ms)

        elapsed_ms = int((time.perf_counter() - start) * 1000)

        if result.returncode != 0:
            error_msg = stderr.strip().split('\n')[-1] if stderr else f'Process exited with code {result.returncode}'
            return _error_response(
                error_msg,
                stdout=stdout,
                stderr=stderr,
                execution_time_ms=elapsed_ms,
            )

        # Read output BEFORE exiting the with block (temp dir is deleted on exit)
        try:
            output_df = pd.read_parquet(output_path)
        except Exception as e:
            return _error_response(
                f'Failed to read output: {e}',
                stdout=stdout,
                stderr=stderr,
                execution_time_ms=elapsed_ms,
            )

        parquet_doc = _persist_parquet(node_item, output_df)

        execution_log = stdout
        if stderr:
            execution_log = f"{stdout}\n[stderr]\n{stderr}".strip() if stdout else f"[stderr]\n{stderr}"

        return {
            'html_table': output_df.head().to_html(index=False),
            'stats': {
                'rows': len(output_df),
                'columns': len(output_df.columns),
                'column_names': list(output_df.columns),
            },
            'parquet_file_id': parquet_doc.id,
            'parquet_file_url': parquet_doc.file.url,
            'parquet_file_title': parquet_doc.title,
            'stdout': stdout,
            'stderr': stderr,
            'execution_log': execution_log,
            'execution_time_ms': elapsed_ms,
            'status': 'success',
        }
