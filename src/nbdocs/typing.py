from pathlib import Path, PosixPath
from typing import Callable, Tuple, TypeVar

from nbconvert.exporters.exporter import ResourcesDict
from nbformat import NotebookNode


PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)
TPreprocessor = Callable[
    [NotebookNode, ResourcesDict], Tuple[NotebookNode, ResourcesDict]
]
