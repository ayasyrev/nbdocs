from pathlib import Path

import typer
from nbdocs.convert import convert2md
from nbdocs.core import get_nb_names
from nbdocs.settings import DOCS_PATH, IMAGES_PATH
from rich import print

app = typer.Typer()


@app.callback(invoke_without_command=True)
def convert(
    ctx: typer.Context,
    filename: Path = typer.Option(None, "-f", "--fn", help="NB filename to convert"),
    dirname: Path = typer.Option(
        None, "-d", "--dir", help="NB directory name to convert"
    ),
    dest_path: Path = typer.Option(None, "--dest", "--dest-path", help="Docs path."),
    image_path: str = typer.Option(None, help="Image path at docs."),
    silent_mode: bool = typer.Option(False, "-s", help="Run in silent mode."),
) -> None:
    """NbDocs. Convert notebooks to docs. Default to .md"""
    if ctx.invoked_subcommand is None:
        dest_path = dest_path or Path(DOCS_PATH)

        nb_names = get_nb_names(filename, dirname)

        if len(nb_names) == 0:
            typer.echo("No files to convert!")
            raise typer.Abort()

        # if convert whole directory, put result to docs subdir.
        if dirname is not None and filename is None:
            dest_path = dest_path / dirname.name

        dest_path.mkdir(parents=True, exist_ok=True)

        image_path = image_path or IMAGES_PATH
        (dest_path / image_path).mkdir(exist_ok=True)

        if not silent_mode:
            print(f"Files to convert from {nb_names[0].parent}:")
            for fn in nb_names:
                print(f"    {fn.name}")
            print(f"Destination directory: {dest_path},\nImage directory: {image_path}")

        convert2md(nb_names, dest_path, image_path)


if __name__ == "__main__":
    app()
