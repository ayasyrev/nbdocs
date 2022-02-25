from pathlib import Path, PosixPath
from typing import Union

import nbformat
from nbformat import NotebookNode
from nbconvert.preprocessors import ClearMetadataPreprocessor

from nbdocs.process import ClearExecutionCountPreprocessor


def read_nb(fn: Union[str, PosixPath], as_version: int = 4) -> NotebookNode:
    """Read notebook from filename.

    Args:
        fn (Union[str, PosixPath): Notebook filename.
        as_version (int, optional): Version of notebook. Defaults to None, convert from 4.

    Returns:
        nbformat.nbformat.NotebookNode: [description]
    """
    with Path(fn).open('r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=as_version)
    nb.filename = fn
    return nb


def write_nb(nb: NotebookNode, fn: Union[str, PosixPath], as_version=nbformat.NO_CONVERT):
    nb.pop('filename', None)
    fn = Path(fn)
    if fn.suffix != '.ipynb':
        fn = fn.with_suffix('.ipynb')
    with fn.open('w') as f:
        nbformat.write(nb, f, version=as_version)


def clean_nb(nb: NotebookNode, clear_execution_count: bool = True) -> None:
    """Clean notebook metadata and execution_count.

    Args:
        nb (NotebookNode): Notebook to clean.
        clear_execution_count (bool, optional): Clear execution_count. Defaults to True.
    """
    cleaner = ClearMetadataPreprocessor(enabled=True)
    nb, _ = cleaner(nb, resources='')
    if clear_execution_count:
        cleaner_execution_count = ClearExecutionCountPreprocessor(enabled=True)
        nb, _ = cleaner_execution_count(nb, resources='')


def clean_nb_file(fn: Union[str, PosixPath],
                  clear_execution_count: bool = True,
                  as_version: int = 4) -> None:
    """Clean metadata and execution count from notebook.

    Args:
        fn (Union[str, PosixPath]): Notebook filename.
        as_version (int, optional): Nbformat version. Defaults to 4.
        clear_execution_count (bool, optional): Clean execution count. Defaults to True.
    """
    nb = read_nb(fn, as_version)
    clean_nb(nb, clear_execution_count)
    write_nb(nb, fn, as_version)
