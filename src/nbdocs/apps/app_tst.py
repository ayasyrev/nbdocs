from pathlib import Path
import typer

app = typer.Typer()


@app.command()
# def main(name: str = typer.Argument(...)):
#     typer.echo(f"Hello {name}")
def nbclean(path: Path = typer.Argument(..., help='Path to NB or folder with Nbs to clean'),
            clear_execution_count: bool = typer.Option(True, '--ec', help='Clean execution counts.')
            ) -> None:
    typer.echo(f"Hello {path}, exist: {path.exists()}")


if __name__ == "__main__":
    # typer.run(main)
    app()
