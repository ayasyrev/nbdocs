from pathlib import Path, PosixPath
from typing import Union

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


def clean_nb(nb: NotebookNode) -> None:
    pass
