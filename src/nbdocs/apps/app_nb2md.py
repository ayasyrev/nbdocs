from pathlib import Path

import typer
from nbdocs.convert import convert2md
from nbdocs.core import get_nb_names
from nbdocs.settings import DOCS_PATH, IMAGES_PATH

app = typer.Typer()


@app.command()
def convert(
    path: Path = typer.Argument(..., help="Path to NB or folder with Nbs to convert"),
    dest_path: Path = typer.Option(None, "--dest", "--dest-path", help="Docs path."),
    image_path: str = typer.Option(None, help="Image path at docs."),
    silent_mode: bool = typer.Option(False, "-s", help="Run in silent mode."),
) -> None:
    """Nb2Md. Convert notebooks to Markdown."""

    nb_names = get_nb_names(path)

    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Abort()

    dest_path = dest_path or Path(DOCS_PATH)

    # if convert whole directory, put result to docs subdir.
    if path is not None and path.is_dir():
        dest_path = dest_path / path.name

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
    # typer.run(convert)
    app()
