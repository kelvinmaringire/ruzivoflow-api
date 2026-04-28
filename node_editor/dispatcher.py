from node_editor.utils.read_csv import read_csv
from node_editor.utils.read_json import read_json
from node_editor.utils.read_excel import read_excel
from node_editor.utils.select_columns import select_columns
from node_editor.utils.save_file import save_file
from node_editor.utils.python_code import python_code

READER_FUNCTIONS = {
    "read_csv": read_csv,
    "read_json": read_json,
    "read_excel": read_excel,
    "select_columns": select_columns,
    "save_file": save_file,
    "python_code": python_code,
}


def get_reader_function(original_id):
    return READER_FUNCTIONS.get(original_id)


