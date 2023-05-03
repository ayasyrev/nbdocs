from pathlib import Path, PosixPath
from typing import (Any, Callable, Dict, List, Optional, Protocol, Tuple, TypeVar,
                    Union, runtime_checkable)

from nbconvert.exporters.exporter import ResourcesDict

PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)

Metadata = Dict[str, Union[str, int, "Metadata"]]  # temp
Source = str  # at nbformat schema: multiline_string -> List[str]. But after read nb we got str.
# Output = TypeVar("Output")


class Output(Protocol):
    output_type: str  # execute_result, display_data, stream, error

    def __getitem__(self, item: str) -> Any:
        ...


class ExecuteResult(Output, Protocol):
    output_type: str = "execute_result"
    data: str  # mimebundle - "A mime-type keyed dictionary of data"
    # "Mimetypes with JSON output, can be any type"
    metadata: Metadata
    execution_count: Optional[int]


class DisplayData(Output, Protocol):
    output_type: str = "display_data"
    data: str  # mimebundle
    metadata: Metadata


class Stream(Output, Protocol):
    output_type: str = "stream"
    name: str  # "The name of the stream (stdout, stderr)."
    text: str


class Error(Output, Protocol):
    output_type: str = "error"
    ename: str  # "The name of the error."
    evalue: str  # "The value, or message, of the error."
    traceback: List[str]


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
