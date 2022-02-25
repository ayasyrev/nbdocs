from pathlib import Path
from typing import List, Union

import typer
from rich import print

from nbdocs.convert import convert2md
from nbdocs.core import clean_nb_file
from nbdocs.settings import DOCS_PATH, IMAGES_PATH, NOTEBOOKS_PATH


app = typer.Typer()


def get_nb_names(filename: Union[Path, None] = None, dirname: Union[Path, None] = None) -> List[Path]:
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
        return list(Path(NOTEBOOKS_PATH).glob('*.ipynb'))

    if filename is not None:
        if filename.is_dir():
            typer.echo(f"Filename must be notebook file, not directory. {filename=}")
            raise typer.Abort()
        if filename.suffix != '.ipynb':
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
        return list(Path(dirname).glob('*.ipynb'))


@app.command()
def cleanfile(filename: Path = typer.Argument(..., help='Nb filename to clean.'),
              clear_execution_count: bool = typer.Option(True, '--ec'), help='Clean execution counts.') -> None:
    """Clean Nb: all metadata and execution counts."""
    nb_names = get_nb_names(filename)
    if len(nb_names) == 0:
        typer.echo('No files to clean!')
        raise typer.Abort()
    typer.echo(f"Clean nb:  {filename}")
    clean_nb_file(nb_names[0], clear_execution_count=clear_execution_count)


@app.command()
def cleandir(dirname: Path = typer.Argument(None, help='NB directory to clean'),
             clear_execution_count: bool = typer.Option(True, '--ec'), help='Clean execution counts.') -> None:
    """Clean Nbs at dir: all metadata and execution counts. Default current dir)."""
    if dirname is None:
        dirname = Path('.')
    nb_names = get_nb_names(dirname=dirname)
    if len(nb_names) == 0:
        typer.echo('No files to clean!')
        raise typer.Abort()
    typer.echo(f"Clean {len(nb_names)} notebooks from dir: {dirname}")
    for nb in nb_names:
        clean_nb_file(nb, clear_execution_count=clear_execution_count)


@app.command()
def clean(clear_execution_count: bool = typer.Option(True, '--ec'), help='Clean execution counts.') -> None:
    """Clean default nb directory - metadata and execution counts from nbs."""
    typer.echo(f"CLEAN DEFAULT Nbs directory: {Path(NOTEBOOKS_PATH)}")
    nb_names = get_nb_names()
    for nb in nb_names:
        clean_nb_file(nb, clear_execution_count)


@app.callback(invoke_without_command=True)
def convert(ctx: typer.Context,
            filename: Path = typer.Option(None, '-f', '--fn', help='NB filename to convert'),
            dirname: Path = typer.Option(None, '-d', '--dir', help='NB directory name to convert'),
            dest_path: Path = typer.Option(None, '--dest', '--dest-path', help='Docs path.'),
            image_path: str = typer.Option(None, help='Image path at docs.'),
            silent_mode: bool = typer.Option(False, '-s', help='Run in silent mode.')
            ) -> None:
    """NbDocs. Convert notebooks to docs. Default to .md
    """
    if ctx.invoked_subcommand is None:
        dest_path = dest_path or Path(DOCS_PATH)

        nb_names = get_nb_names(filename, dirname)

        if len(nb_names) == 0:
            typer.echo('No files to convert!')
            raise typer.Abort()

        # if convert whole directory, put result to docs subdir.
        if dirname is not None and filename is None:
            dest_path = dest_path / dirname.name

        dest_path.mkdir(parents=True, exist_ok=True)

        image_path = image_path or IMAGES_PATH
        (dest_path / image_path).mkdir(exist_ok=True)

        if not silent_mode:
            print(f'Files to convert from {nb_names[0].parent}:')
            for fn in nb_names:
                print(f"    {fn.name}")
            print(f'Destination directory: {dest_path},\nImage directory: {image_path}')

        convert2md(nb_names, dest_path, image_path)


if __name__ == "__main__":
    app()
