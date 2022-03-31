from pathlib import Path

import typer
from nbdocs.clean import clean_nb_file
from nbdocs.core import get_nb_names
from nbdocs.settings import NOTEBOOKS_PATH

app = typer.Typer()


@app.command()
def nbclean(
    path: Path = typer.Argument(None, help="Path to NB or folder with Nbs to clean"),
    clear_execution_count: bool = typer.Option(
        True, "--ec", help="Clean execution counts."
    ),
) -> None:
    """Clean Nb or notebooks at `path` - metadata and execution counts from nbs."""
    path = path or Path(NOTEBOOKS_PATH)

    nb_names = get_nb_names(path)

    if len(nb_names) == 0:
        typer.echo("No files to clean!")
        raise typer.Abort()

    typer.echo(f"Clean: {path}")

    for nb in nb_names:
        clean_nb_file(nb, clear_execution_count)


if __name__ == "__main__":
    app()
