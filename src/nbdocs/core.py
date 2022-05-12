from pathlib import Path, PosixPath
from typing import List, Union

import nbformat
import typer
from nbformat import NotebookNode

from nbdocs.settings import NOTEBOOKS_PATH, DOCS_PATH


def read_nb(fn: Union[str, PosixPath], as_version: int = 4) -> NotebookNode:
    """Read notebook from filename.

    Args:
        fn (Union[str, PosixPath): Notebook filename.
        as_version (int, optional): Version of notebook. Defaults to None, convert from 4.

    Returns:
        nbformat.nbformat.NotebookNode: [description]
    """
    with Path(fn).open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=as_version)
    nb.filename = fn
    return nb


def write_nb(
    nb: NotebookNode, fn: Union[str, PosixPath], as_version=nbformat.NO_CONVERT
) -> None:
    """Write notebook to file

    Args:
        nb (NotebookNode): Notebook to write
        fn (Union[str, PosixPath]): filename to write
        as_version (_type_, optional): Nbformat version. Defaults to nbformat.NO_CONVERT.
    Returns:
        PosixPath: Filename of writed Nb.
    """
    nb.pop("filename", None)
    fn = Path(fn)
    if fn.suffix != ".ipynb":
        fn = fn.with_suffix(".ipynb")
    with fn.open("w", encoding="utf-8") as fh:
        nbformat.write(nb, fh, version=as_version)
    return fn


def get_nb_names(path: Union[Path, str, None] = None) -> List[Path]:
    """Return list of notebooks from `path`. If no `path` return notebooks from default folder.

    Args:
        path (Union[Path, str, None]): Path for nb or folder with notebooks.

    Raises:
        typer.Abort: If filename or dir not exists or not nb file.

    Returns:
        List[Path]: List of notebooks names.
    """
    path = path or NOTEBOOKS_PATH  # Default - process nbs dir.
    path = Path(path)

    if not path.exists():
        typer.echo(f"{path} not exists!")
        raise typer.Abort()

    if path.is_dir():
        return list(path.glob("*.ipynb"))

    if path.suffix != ".ipynb":
        typer.echo(f"Nb extension must be .ipynb, but got: {path.suffix}")
        raise typer.Abort()

    return [path]


def filter_changed(nb_names: List[Path], docs_path: Path = None) -> List[Path]:
    """Filter list of Nb to changed only (compare modification date with dest name).

    Args:
        nb_names (List[Path]): List of Nb filenames.
        dest (Path, optional): Destination folder for md files.
            If not given default from settings. Defaults to None.

    Returns:
        List[Path]: List of Nb filename with newer modification time.
    """
    docs_path = docs_path or Path(DOCS_PATH)
    return [
        nb_name
        for nb_name in nb_names
        if not (md_name := (docs_path / nb_name.name).with_suffix(".md")).exists()
        or nb_name.stat().st_mtime >= md_name.stat().st_mtime
    ]
