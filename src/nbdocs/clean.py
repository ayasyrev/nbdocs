from pathlib import PosixPath
from typing import List, Tuple, Union

from nbconvert.exporters.exporter import ResourcesDict
from nbconvert.preprocessors import ClearMetadataPreprocessor, Preprocessor
from nbformat import NotebookNode

from nbdocs.core import read_nb, write_nb


class ClearExecutionCountPreprocessor(Preprocessor):
    """
    Clear execution_count from all code cells in a notebook.
    """

    def preprocess_cell(self, cell: NotebookNode, resources: ResourcesDict, index: int):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "code":
            cell.execution_count = None
            for output in cell.outputs:
                if "execution_count" in output:
                    output.execution_count = None
        return cell, resources


class MetadataCleaner:
    """Metadata cleaner.
    Wrapper for meatada and execution count preprocessors.
    """

    def __init__(self) -> None:
        self.cleaner_metadata = ClearMetadataPreprocessor(enabled=True)
        self.cleaner_execution_count = ClearExecutionCountPreprocessor(enabled=True)

    def __call__(
        self,
        nb: NotebookNode,
        resources: ResourcesDict = None,
        clear_execution_count: bool = True,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        nb, resources = self.cleaner_metadata(nb, resources)
        if clear_execution_count:
            nb, resources = self.cleaner_execution_count(nb, resources)
        return nb, resources


def clean_nb(nb: NotebookNode, clear_execution_count: bool = True) -> None:
    """Clean notebook metadata and execution_count.

    Args:
        nb (NotebookNode): Notebook to clean.
        clear_execution_count (bool, optional): Clear execution_count. Defaults to True.
    """
    cleaner = MetadataCleaner()
    nb, _ = cleaner(nb, ResourcesDict(), clear_execution_count)


def clean_nb_file(
    fn: Union[str, PosixPath, List[Union[str, PosixPath]]],
    clear_execution_count: bool = True,
    as_version: int = 4,
) -> None:
    """Clean metadata and execution count from notebook.

    Args:
        fn (Union[str, PosixPath]): Notebook filename or list of names.
        as_version (int, optional): Nbformat version. Defaults to 4.
        clear_execution_count (bool, optional): Clean execution count. Defaults to True.
    """
    cleaner = MetadataCleaner()
    resources = ResourcesDict()
    if not isinstance(fn, list):
        fn = [fn]
    for fn_item in fn:
        nb = read_nb(fn_item, as_version)
        nb, _ = cleaner(nb, resources, clear_execution_count)
        write_nb(nb, fn_item, as_version)  # to do: write only if nb cleaned (modify resources if cleaned metadata)
