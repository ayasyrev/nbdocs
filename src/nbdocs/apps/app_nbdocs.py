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
    nbs_number = len(nb_names)
    if nbs_number == 0:
        typer.echo("No files to convert!")
        raise typer.Exit()
    typer.echo(f"Found {nbs_number} notebooks.")
    if not force:
        message = "Filtering notebooks with changes... "
        nb_names = filter_changed(nb_names, cfg)
        if len(nb_names) == nbs_number:
            message += "No changes."
        typer.echo(message)

    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Exit()

    typer.echo(f"To convert: {len(nb_names)} notebooks.")
    convert2md(nb_names, cfg)


if __name__ == "__main__":
    app()
