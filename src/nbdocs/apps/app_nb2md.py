from pathlib import Path
import typer
from nbdocs.convert import convert2md, filter_changed
from nbdocs.core import get_nb_names
from nbdocs.settings import get_config

app = typer.Typer()


@app.command()
def convert(
    nb_path: str = typer.Argument(..., help="Path to NB or folder with Nbs to convert"),
    dest_path: str = typer.Option(None, "--dest", "--dest-path", help="Docs path."),
    images_path: str = typer.Option(None, help="Image path at docs."),
    force: bool = typer.Option(
        False, "-F", "--force", help="Force convert all notebooks."
    ),
    silent_mode: bool = typer.Option(False, "-s", help="Run in silent mode."),
) -> None:
    """Nb2Md. Convert notebooks to Markdown."""
    nb_names = get_nb_names(nb_path)
    if len(nb_names) == 0:
        typer.echo("No files to convert!")
        raise typer.Exit()

    cfg = get_config(
        notebooks_path=nb_path, docs_path=dest_path, images_path=images_path
    )

    # check logic -> do we need subdir and how to check modified Nbs
    # if convert whole directory, put result to docs subdir.
    if (path := Path(nb_path)).is_dir():
        cfg.docs_path = f"{cfg.docs_path}/{path.name}"
    Path(cfg.docs_path).mkdir(parents=True, exist_ok=True)
    (Path(cfg.docs_path) / cfg.images_path).mkdir(exist_ok=True)

    if not force:
        nb_names = filter_changed(nb_names, cfg)

    if len(nb_names) == 0:
        typer.echo("No files with changes to convert!")
        raise typer.Exit()

    if not silent_mode:
        print(f"Files to convert from {nb_names[0].parent}:")
        for fn in nb_names:
            print(f"    {fn.name}")
        print(
            f"Destination directory: {dest_path},\nImage directory: {cfg.images_path}"
        )

    convert2md(nb_names, cfg)


if __name__ == "__main__":  # pragma: no cover
    app()
