from pathlib import Path

import typer

from nbdocs.convert import convert2md
from nbdocs.core import get_nb_names
from nbdocs.settings import DOCS_PATH, IMAGES_PATH

app = typer.Typer()


@app.callback()
def convert() -> None:
    """NbDocs. Convert notebooks to docs. Default to .md"""
    nb_names = get_nb_names()
    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Abort()

    dest_path = Path(DOCS_PATH)
    dest_path.mkdir(parents=True, exist_ok=True)

    image_path = IMAGES_PATH
    (dest_path / image_path).mkdir(exist_ok=True)

    convert2md(nb_names, dest_path, image_path)


if __name__ == "__main__":
    app()
