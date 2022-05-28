from pathlib import Path

import typer

from nbdocs.convert import convert2md
from nbdocs.core import filter_changed, get_nb_names
from nbdocs.settings import get_config

app = typer.Typer()


@app.command()
def convert(
    force: bool = typer.Option(
        False, "-F", "--force", help="Force convert all notebooks."
    ),
) -> None:
    """NbDocs. Convert notebooks to docs. Default to .md"""
    cfg = get_config()
    path = cfg["notebooks_path"]
    nb_names = get_nb_names(path)
    dest_path = Path(cfg["docs_path"])
    if not force:
        nb_names = filter_changed(nb_names, dest_path)

    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Exit()

    image_path = cfg["images_path"]

    convert2md(nb_names, dest_path, image_path)


if __name__ == "__main__":
    app()
