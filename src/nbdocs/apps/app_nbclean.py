import typer
from nbdocs.clean import clean_nb_file
from nbdocs.core import get_nb_names
from nbdocs.settings import get_config

app = typer.Typer()


@app.command()
def nbclean(
    nb_path: str = typer.Argument(None, help="Path to NB or folder with Nbs to clean"),
    clear_execution_count: bool = typer.Option(
        True, "--ec", help="Clean execution counts."
    ),
) -> None:
    """Clean Nb or notebooks at `path` - metadata and execution counts from nbs."""
    cfg = get_config(notebooks_path=nb_path)

    nb_names = get_nb_names(cfg.notebooks_path)

    if (num_nbs := len(nb_names)) == 0:
        typer.echo("No files to clean!")
        raise typer.Abort()

    typer.echo(f"Clean: {cfg.notebooks_path}, found {num_nbs} notebooks.")

    clean_nb_file(nb_names, clear_execution_count)


if __name__ == "__main__":  # pragma: no cover
    app()
