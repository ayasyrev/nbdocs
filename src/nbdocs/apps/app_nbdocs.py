from pathlib import Path

import typer

from nbdocs.convert import convert2md
from nbdocs.core import filter_changed, get_nb_names
from nbdocs.settings import nbdocs_def_cfg

app = typer.Typer()


@app.command()
def convert(
    force: bool = typer.Option(
        False, "-F", "--force", help="Force convert all notebooks."
    ),
) -> None:
    """NbDocs. Convert notebooks to docs. Default to .md"""
    nb_names = get_nb_names()
    dest_path = Path(nbdocs_def_cfg["docs_path"])
    if not force:
        nb_names = filter_changed(nb_names, dest_path)

    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Exit()

    image_path = nbdocs_def_cfg["images_path"]

    convert2md(nb_names, dest_path, image_path)


if __name__ == "__main__":
    app()
