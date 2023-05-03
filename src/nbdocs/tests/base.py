from pathlib import Path, PosixPath
from typing import List, Optional, Union

from nbformat import v4 as nbformat

from nbdocs.typing import Nb, Cell, CodeCell, MarkdownCell, Metadata


def create_code_cell(source: str) -> CodeCell:
    """Create basic code cell with given source.
    Outputs basic text data.

    Args:
        source (str): Source for code cell

    Returns:
        Cell: Nb code cell.
    """
    outputs = [
        nbformat.new_output(  # type: ignore
            "display_data", data={"text/plain": "- test/plain in output"}
        ),
        nbformat.new_output(  # type: ignore
            "stream", name="stdout", text="- text in stdout (stream) output"
        ),
        nbformat.new_output("display_data", data={"image/png": "Zw=="}),  # type: ignore
    ]
    return nbformat.new_code_cell(source=source, outputs=outputs)  # type: ignore


def create_markdown_cell(source: str) -> MarkdownCell:
    """Create basic markdown cell with given source.

    Args:
        source (str): Source ror markdown cell

    Returns:
        Cell: Nb markdown cell.
    """
    return nbformat.new_markdown_cell(source)  # type: ignore


def create_nb(
    code_source: Optional[str] = None, md_source: Optional[str] = None
) -> Nb:
    """Create basic test nb.

    Args:
        code_source (str, optional): Source for code cell. Defaults to None.
        md_source (str, optional): Source for markdown cell. Defaults to None.

    Returns:
        Cell: Nb for test
    """
    cells: List[Cell] = []
    if code_source is not None:
        cells.append(create_code_cell(code_source))
    if md_source is not None:
        cells.append(create_markdown_cell(md_source))
    return nbformat.new_notebook(cells=cells)  # type: ignore


def create_cell_metadata(
    cell: Cell,
    execution_count: Optional[int] = None,
    metadata: Optional[Metadata] = None,
) -> None:
    """Fill cell with metadata.

    Args:
        cell (Cell): Cell to process.
        execution_count (int, optional): Execution count. If None than 1. Defaults to None.
        metadata (dict, optional): Metadata to fill. If None, used default set. Defaults to None.
    """
    if cell.cell_type == "code":
        execution_count = execution_count or 1
        cell.execution_count = execution_count
        if len(cell.outputs) > 0:
            cell.outputs[0].execution_count = execution_count
        default_metadata = {}
        default_metadata["test_field"] = "test_value"
        default_metadata["executeTime"] = dict(
            [("end_time", "09:31:50"), ("start_time", "09:31:49")]
        )
        metadata = metadata or default_metadata
        # if "metadata" not in cell:  # metadata is required at cell
        #     cell.metadata = {}
        cell.metadata.update(metadata)


def create_nb_metadata(nb: Nb, metadata: Optional[Metadata] = None) -> None:
    """Fill nb metadata

    Args:
        nb (Cell): Nb to process.
        metadata (dict, optional): Metadata to set. Defaults to None.
    """
    metadata = metadata or {
        "language_info": {"name": "python", "version": "3.9"},
        "kernelspec": {"language": "python", "name": "python3"},
    }
    nb.metadata = metadata


def create_tmp_image_file(image_name: Union[PosixPath, Path]) -> None:
    """Create tmp image file.

    Args:
        image_name (PosixPath): Image name
    """
    with open(image_name, "wb") as fh:
        fh.write(b"X===")
