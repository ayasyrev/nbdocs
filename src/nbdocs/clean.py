from pathlib import PosixPath
from typing import Union

from nbconvert.preprocessors import ClearMetadataPreprocessor, Preprocessor
from nbformat import NotebookNode

from nbdocs.core import read_nb, write_nb


class ClearExecutionCountPreprocessor(Preprocessor):
    """
    Clear execution_count from all code cells in a notebook.
    """

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "code":
            cell.execution_count = None
            for output in cell.outputs:
                if "execution_count" in output:
                    output.execution_count = None
        return cell, resources


def clean_nb(nb: NotebookNode, clear_execution_count: bool = True) -> None:
    """Clean notebook metadata and execution_count.

    Args:
        nb (NotebookNode): Notebook to clean.
        clear_execution_count (bool, optional): Clear execution_count. Defaults to True.
    """
    cleaner = ClearMetadataPreprocessor(enabled=True)
    nb, _ = cleaner(nb, resources="")
    if clear_execution_count:
        cleaner_execution_count = ClearExecutionCountPreprocessor(enabled=True)
        nb, _ = cleaner_execution_count(nb, resources="")


def clean_nb_file(
    fn: Union[str, PosixPath], clear_execution_count: bool = True, as_version: int = 4
) -> None:
    """Clean metadata and execution count from notebook.

    Args:
        fn (Union[str, PosixPath]): Notebook filename.
        as_version (int, optional): Nbformat version. Defaults to 4.
        clear_execution_count (bool, optional): Clean execution count. Defaults to True.
    """
    nb = read_nb(fn, as_version)
    clean_nb(nb, clear_execution_count)
    write_nb(nb, fn, as_version)
