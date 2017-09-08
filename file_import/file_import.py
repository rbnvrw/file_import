"""
Load a file from a path
"""
from types import SimpleNamespace
from os import path
import inspect


def load(file_path, import_only=None):
    """
    Load a file from path
    """
    result = {}

    file_path = _normalize_path(file_path)

    with open(file_path) as script_file:
        code = compile(script_file.read(), file_path, 'exec')
        exec(code, result)

    if import_only is not None:
        result = {k: result[k] for k in set(import_only) & set(result.keys())}

    result = SimpleNamespace(**result)

    return result


def _normalize_path(file_path):
    """
    Fix the path
    """
    if path.isabs(file_path):
        return file_path

    # fetch original filename from stack
    original_file = inspect.stack()[2][1]
    original_directory = path.dirname(original_file)

    return path.join(original_directory, file_path)
