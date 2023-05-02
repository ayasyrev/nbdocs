from pathlib import Path, PosixPath
from typing import Callable, List, Tuple, TypeVar, Union

import nbformat
import typer
from nbconvert.exporters.exporter import ResourcesDict
from nbformat import NotebookNode


PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)
TPreprocessor = Callable[
    [NotebookNode, ResourcesDict], Tuple[NotebookNode, ResourcesDict]
]


def read_nb(
    fn: PathOrStr, as_version: nbformat.Sentinel = nbformat.NO_CONVERT
) -> NotebookNode:
    """Read notebook from filename.

    Args:
        fn (Union[str, PosixPath): Notebook filename.
        as_version (int, optional): Version of notebook. Defaults to None, convert from 4.

    Returns:
        nbformat.nbformat.NotebookNode: [description]
    """
    with Path(fn).open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=as_version)
    return nb


def write_nb(
    nb: NotebookNode,
    fn: PathOrStr,
    as_version: nbformat.Sentinel = nbformat.NO_CONVERT,
) -> Path:
    """Write notebook to file

    Args:
        nb (NotebookNode): Notebook to write
        fn (Union[str, PosixPath]): filename to write
        as_version (_type_, optional): Nbformat version. Defaults to nbformat.NO_CONVERT.
    Returns:
        Path: Filename of writed Nb.
    """
    filename = Path(fn)
    if filename.suffix != ".ipynb":
        filename = filename.with_suffix(".ipynb")
    with filename.open("w", encoding="utf-8") as fh:
        nbformat.write(nb, fh, version=as_version)
    return filename


def get_nb_names(nb_path: Union[PathOrStr, None] = None) -> List[Path]:
    """Return list of notebooks from `path`. If no `path` return notebooks from current folder.

    Args:
        nb_path (Union[Path, str, None]): Path for nb or folder with notebooks.

    Raises:
        typer.Abort: If filename or dir not exists or not nb file.

    Returns:
        List[Path]: List of notebooks names.
    """
    path = Path(nb_path or ".")

    if not path.exists():
        typer.echo(f"{path} not exists!")
        raise typer.Abort()  # ? may be just exit?

    if path.is_dir():
        return list(path.glob("*.ipynb"))

    if path.suffix != ".ipynb":
        typer.echo(f"Nb extension must be .ipynb, but got: {path.suffix}")
        raise typer.Abort()  # ? may be just exit?

    return [path]
