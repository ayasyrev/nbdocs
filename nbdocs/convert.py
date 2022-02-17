from pathlib import Path
from typing import List, Optional

import nbconvert
import typer
from nbformat import NotebookNode
from rich import print

from nbdocs.core import read_nb
from nbdocs.process import correct_markdown_image_link, correct_output_image_link

# todo: read from config, take care last backslash
NOTEBOOKS_PATH = 'nbs'
DOCS_PATH = 'tmp_docs/docs'
IMAGES_PATH = 'images'


def convert2md(filenames: List[Path], dest_path: Path, image_path: str):
    md_exporter = nbconvert.MarkdownExporter()
    for nb_fn in filenames:
        nb = read_nb(nb_fn)
        correct_markdown_image_link(nb, nb_fn, dest_path, image_path)
        (md, resources) = md_exporter.from_notebook_node(nb)
        dest_fn = dest_path / nb_fn.with_suffix('.md').name

        print(dest_fn)
        if len(resources['outputs']) > 0:
            dest_images = f"{image_path}/{nb_fn.stem}_files"
            (dest_path / dest_images).mkdir(exist_ok=True)
            print(dest_images)
            for image_name, image_data in resources['outputs'].items():
                print(image_name, dest_path / dest_images / image_name)
                with open(dest_path / dest_images / image_name, 'wb') as f:
                    md = correct_output_image_link(image_name, dest_images, md)
                    f.write(image_data)
        
        with open(dest_fn, 'w') as f:
            f.write(md)


def main(
    filename: Optional[Path] = typer.Argument(None),
    dest_path: Optional[Path] = typer.Option(None, '--dest', '--dest-path'),
    image_path: Optional[str] = typer.Option(None)
    ):
    if filename is None:
        filename = Path(NOTEBOOKS_PATH)
        filename = list(filename.glob('*.ipynb'))  # need recursive?
    elif filename.is_dir():
        filename = list(filename.glob('*.ipynb'))  # need recursive?
    else:
        if not filename.exists():
            typer.echo(f"{filename} not exists!")
            raise typer.Abort()
        else:
            filename = [filename]

    if len(filename) == 0:
        typer.echo('No files to convert!')
        raise typer.Abort()

    print(f'Files to convert from {filename[0].parent}:')
    for fn in filename:
        print(f"    {fn.name}")
    
    dest_path = dest_path or Path(DOCS_PATH)
    if not dest_path.exists():
        dest_path.mkdir(parents=True)
    image_path = image_path or IMAGES_PATH
    if not (dest_path / image_path).exists():
        (dest_path / image_path).mkdir()

    print(f'Docs directory: {dest_path},\nImage directory: {image_path}')

    convert2md(filename, dest_path, image_path)


if __name__ == '__main__':
    typer.run(main)
