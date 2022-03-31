from pathlib import Path, PosixPath
from typing import List, Union

import nbformat
import typer
from nbformat import NotebookNode

from nbdocs.settings import NOTEBOOKS_PATH


def read_nb(fn: Union[str, PosixPath], as_version: int = 4) -> NotebookNode:
    """Read notebook from filename.

    Args:
        fn (Union[str, PosixPath): Notebook filename.
        as_version (int, optional): Version of notebook. Defaults to None, convert from 4.

    Returns:
        nbformat.nbformat.NotebookNode: [description]
    """
    with Path(fn).open("r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=as_version)
    nb.filename = fn
    return nb


def write_nb(
    nb: NotebookNode, fn: Union[str, PosixPath], as_version=nbformat.NO_CONVERT
):
    nb.pop("filename", None)
    fn = Path(fn)
    if fn.suffix != ".ipynb":
        fn = fn.with_suffix(".ipynb")
    with fn.open("w") as f:
        nbformat.write(nb, f, version=as_version)


def get_nb_names(path: Union[Path, None] = None) -> List[Path]:
    """Return list of notebooks from `path`. If no `path` return notebooks from default folder.

    Args:
        path (Union[Path, None]): Path for nb or folder with notebooks.

    Raises:
        typer.Abort: If filename or dir not exists or not nb file.

    Returns:
        List[Path]: List of notebooks names.
    """
    path = path or Path(NOTEBOOKS_PATH)  # Default - process nbs dir.

    if not path.exists():
        typer.echo(f"{path} not exists!")
        raise typer.Abort()

    if path.is_dir():
        return list(path.glob("*.ipynb"))

    if path.suffix != ".ipynb":
        typer.echo(f"Nb extension must be .ipynb, but got: {path.suffix}")
        raise typer.Abort()

    return [path]


def _get_nb_names(
    filename: Union[Path, None] = None, dirname: Union[Path, None] = None
) -> List[Path]:
    """Check filename, dirname and return list of notebooks.

    Args:
        filename (Union[Path, None]): Notebook name
        dirname (Union[Path, None]): Directory with notebooks.

    Raises:
        typer.Abort: If filename or dir not exists.

    Returns:
        List[Path]: List of notebooks names.
    """
    if filename is None and dirname is None:
        # Default - process nbs dir.
        return list(Path(NOTEBOOKS_PATH).glob("*.ipynb"))

    if filename is not None:
        if filename.is_dir():
            typer.echo(f"Filename must be notebook file, not directory. {filename=}")
            raise typer.Abort()
        if filename.suffix != ".ipynb":
            typer.echo(f"Nb extension must be .ipynb, but got: {filename.suffix}")
            raise typer.Abort()
        if not filename.exists():
            typer.echo(f"{filename} not exists!")
            raise typer.Abort()
        if dirname is not None:
            typer.echo("Used '-f' or '--fn' option, '-d' or '--dir' will be skipped.")
        return [filename]

    if dirname is not None:
        if not dirname.is_dir():
            typer.echo(f"'-d' or '--dir' must be directory. {dirname}")
            raise typer.Abort()
        return list(Path(dirname).glob("*.ipynb"))
