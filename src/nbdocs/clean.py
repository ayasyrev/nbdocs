from typing import List, Optional, Tuple, Union

from nbconvert.exporters.exporter import ResourcesDict
from nbconvert.preprocessors import ClearMetadataPreprocessor, Preprocessor
from nbformat import NotebookNode
import nbformat

from nbdocs.core import PathOrStr, read_nb, write_nb


class ClearMetadataPreprocessorRes(ClearMetadataPreprocessor):
    """ClearMetadata Preprocessor same as at nbconvert
    but return True at resources.changed if nb changed."""

    def preprocess_cell(self, cell, resources, cell_index):
        """
        All the code cells are returned with an empty metadata field.
        """
        if self.clear_cell_metadata:
            if cell.cell_type == 'code':
                # Remove metadata
                if 'metadata' in cell:
                    current_metadata = cell.metadata
                    cell.metadata = dict(self.nested_filter(cell.metadata.items(), self.preserve_cell_metadata_mask))
                    if cell.metadata != current_metadata:
                        resources["changed"] = True
        return cell, resources

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply on each notebook.
        
        Must return modified nb, resources.
        
        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        if self.clear_notebook_metadata:
            if 'metadata' in nb:
                current_metadata = nb.metadata
                nb.metadata = dict(self.nested_filter(nb.metadata.items(), self.preserve_nb_metadata_mask))
                if nb.metadata != current_metadata:
                    resources["changed"] = True
        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources


class ClearExecutionCountPreprocessor(Preprocessor):
    """
    Clear execution_count from all code cells in a notebook.
    """

    def preprocess_cell(self, cell: NotebookNode, resources: ResourcesDict, index: int):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "code":
            if cell.execution_count is not None:
                cell.execution_count = None
                resources["changed"] = True
            for output in cell.outputs:
                if "execution_count" in output:
                    if output.execution_count is not None:
                        output.execution_count = None
                        resources["changed"] = True
        return cell, resources


class MetadataCleaner:
    """Metadata cleaner.
    Wrapper for metadata and execution count preprocessors.
    """

    def __init__(self) -> None:
        self.cleaner_metadata = ClearMetadataPreprocessorRes(enabled=True)
        self.cleaner_execution_count = ClearExecutionCountPreprocessor(enabled=True)

    def __call__(
        self,
        nb: NotebookNode,
        resources: Optional[ResourcesDict] = None,
        clear_execution_count: bool = True,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if resources is None:
            resources = ResourcesDict()
        nb, resources = self.cleaner_metadata(nb, resources)
        if clear_execution_count:
            nb, resources = self.cleaner_execution_count(nb, resources)
        return nb, resources


def clean_nb(nb: NotebookNode, clear_execution_count: bool = True) -> Tuple[NotebookNode, ResourcesDict]:
    """Clean notebook metadata and execution_count.

    Args:
        nb (NotebookNode): Notebook to clean.
        clear_execution_count (bool, optional): Clear execution_count. Defaults to True.
    """
    cleaner = MetadataCleaner()
    return cleaner(nb, clear_execution_count=clear_execution_count)


def clean_nb_file(
    fn: Union[PathOrStr, List[PathOrStr]],
    clear_execution_count: bool = True,
    as_version: nbformat.Sentinel = nbformat.NO_CONVERT,
) -> None:
    """Clean metadata and execution count from notebook.

    Args:
        fn (Union[str, PosixPath]): Notebook filename or list of names.
        as_version (int, optional): Nbformat version. Defaults to 4.
        clear_execution_count (bool, optional): Clean execution count. Defaults to True.
    """
    cleaner = MetadataCleaner()
    if not isinstance(fn, list):
        fn = [fn]
    for fn_item in fn:
        nb = read_nb(fn_item, as_version)
        nb, resources = cleaner(nb, clear_execution_count=clear_execution_count)
        if resources["changed"]:
            write_nb(
                nb, fn_item, as_version
            )
            print(f"done: {fn_item}")
