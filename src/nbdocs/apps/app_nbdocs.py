import typer

from nbdocs.convert import convert2md, filter_changed
from nbdocs.core import get_nb_names
from nbdocs.settings import get_config

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def nbdocs(
    force: bool = typer.Option(
        False, "-F", "--force", help="Force convert all notebooks."
    ),
) -> None:
    """NbDocs. Convert notebooks to docs. Default to .md"""
    cfg = get_config()
    nb_names = get_nb_names(cfg.notebooks_path)
    if not force:
        nb_names = filter_changed(nb_names, cfg)

    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Exit()

    convert2md(nb_names, cfg)


if __name__ == "__main__":
    app()
