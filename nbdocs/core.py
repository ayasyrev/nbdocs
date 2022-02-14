import re
from pathlib import Path, PosixPath
from typing import List, Union

import nbformat
from nbformat import NotebookNode


def read_nb(fn: Union[str, PosixPath], as_version: int = None) -> NotebookNode:
    """Read notebook from filename.

    Args:
        fn (Union[str, PosixPath): Notebook filename.
        as_version (int, optional): Version of notebook. Defaults to None, convert from 4.

    Returns:
        nbformat.nbformat.NotebookNode: [description]
    """
    as_version = as_version or 4
    with open(Path(fn), 'r', encoding='utf8') as f:
        return nbformat.reads(f.read(), as_version=as_version)


HIDE_FLAGS = [
    'hide',  # hide cell
    'hide_input',  # hide code from this cell
    'hide_output'  # hide output from this cell
]


FLAGS = [] + HIDE_FLAGS  # here will be more flags.


def generate_flags_pattern(flags: List[str]) -> str:
    """Generate re pattern from list of flags, add flags with '-' instead of '_'.

    Args:
        flags (List[str]): List of flags 

    Returns:
        str: flags, separated by '|'
    """
    for item in flags.copy():
        if '_' in item:
            flags.append(item.replace('_', '-'))
    return '|'.join(flags)


re_flags = re.compile(  # flags at start of line, after #
    rf"^\s*\#\s*{generate_flags_pattern(FLAGS)}", re.MULTILINE)


def cell_check_flags(cell: NotebookNode) -> bool:
    """Check if cell has nbdocs flags.

    Args:
        cell (NotebookNode): Cell to check.

    Returns:
        bool.
    """
    result = False
    if cell.cell_type == 'code':
        result = re_flags.search(cell.source) is not None
    return result


def clean_nb(nb: NotebookNode) -> None:
    pass
