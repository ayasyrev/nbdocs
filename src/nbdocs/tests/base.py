from pathlib import Path, PosixPath
from typing import List, Optional, Union

from nbformat import v4 as nbformat

from nbdocs.typing import Nb, Cell, CodeCell, MarkdownCell, Metadata, Output


test_outputs = [
    nbformat.new_output(  # type: ignore
        "display_data", data={"text/plain": "- test/plain in output"}
    ),
    nbformat.new_output(  # type: ignore
        "stream", name="stdout", text="- text in stdout (stream) output"
    ),
    nbformat.new_output("display_data", data={"image/png": "Zw=="}),  # type: ignore
]


def create_code_cell(
        source: str,
        outputs: Optional[List[Output]] = None,
) -> CodeCell:
    """Create basic code cell with given source.
    Outputs basic text data.

    Args:
        source (str): Source for code cell
        outputs (Optional[List[Output]], optional): Outputs. Defaults to None.

    Returns:
        Cell: Nb code cell.
    """
    cell_create_kwargs = {"source": source}
    if outputs is not None:
        cell_create_kwargs["outputs"] = outputs
    return nbformat.new_code_cell(**cell_create_kwargs)


def create_markdown_cell(source: str) -> MarkdownCell:
    """Create basic markdown cell with given source.

    Args:
        source (str): Source ror markdown cell

    Returns:
        Cell: Nb markdown cell.
    """
    return nbformat.new_markdown_cell(source)  # type: ignore


def create_nb(
    code_source: Optional[str] = None,
    md_source: Optional[str] = None,
    code_outputs: Optional[List[Output]] = None,
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
        cells.append(create_code_cell(code_source, code_outputs))
    if md_source is not None:
        cells.append(create_markdown_cell(md_source))
    return nbformat.new_notebook(cells=cells)  # type: ignore


def create_cell_metadata(
    cell: Cell,
    metadata: Metadata,
    execution_count: Optional[int] = None,
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

    cell.metadata.update(metadata)


def create_nb_metadata(nb: Nb, metadata: Metadata) -> None:
    """Fill nb metadata

    Args:
        nb (Nb): Nb to process.
        metadata (dict, optional): Metadata to set.
    """
    nb.metadata = metadata


def create_tmp_image_file(image_name: Union[PosixPath, Path]) -> None:
    """Create tmp image file.

    Args:
        image_name (PosixPath): Image name
    """
    with open(image_name, "wb") as fh:
        fh.write(b"X===")
