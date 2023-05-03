from pathlib import Path, PosixPath
from typing import (Callable, Dict, List, Optional, Protocol, Tuple, TypeVar,
                    Union, runtime_checkable)

from nbconvert.exporters.exporter import ResourcesDict

PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)

Metadata = Dict[str, Union[str, int, "Metadata"]]  # temp
Source = str  # at nbformat schema: multiline_string -> List[str]. But after read nb we got str.
Output = TypeVar("Output")


@runtime_checkable
class Cell(Protocol):
    """Notebook cell protocol."""
    id: int  # check
    cell_type: str
    metadata: Metadata
    source: Source


class CodeCell(Cell):
    """Code_cell protocol."""
    id: int
    cell_type = "code"
    metadata: Metadata
    source: Source
    outputs: List[Output]
    execution_count: Optional[int]


class MarkdownCell(Cell):
    """Markdown_cell protocol."""
    id: int
    cell_type = "markdown"
    metadata: Metadata
    source: Source


class RawCell(Cell):
    """Raw_cell protocol."""
    id: int
    cell_type = "raw"
    metadata: Metadata
    source: Source


@runtime_checkable
class Nb(Protocol):
    """Notebook protocol."""
    nbformat: int
    nbformat_minor: int
    cells: List[Cell]
    metadata: Metadata


NbAndResources = Tuple[Nb, ResourcesDict]
CellAndResources = Tuple[Cell, ResourcesDict]

TPreprocessor = Callable[[Nb, ResourcesDict], NbAndResources]
