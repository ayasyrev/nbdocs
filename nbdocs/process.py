import re
import shutil
from pathlib import Path
from typing import List

from nbformat import NotebookNode

HIDE_FLAGS = [
    'hide',  # hide cell
    'hide_input',  # hide code from this cell
    'hide_output'  # hide output from this cell
]


FLAGS = [] + HIDE_FLAGS  # here will be more flags.


def generate_flags_pattern(flags: List[str]) -> str:
    """Generate re pattern from list of flags, add flags with '-' instead of '_'.

    Args:
        flags (List[str]): List of flags 

    Returns:
        str: flags, separated by '|'
    """
    for item in flags.copy():
        if '_' in item:
            flags.append(item.replace('_', '-'))
    return '|'.join(flags)


re_flags = re.compile(  # flags at start of line, after #
    rf"^\s*\#\s*{generate_flags_pattern(FLAGS)}", re.MULTILINE)


def cell_check_flags(cell: NotebookNode) -> bool:
    """Check if cell has nbdocs flags.

    Args:
        cell (NotebookNode): Cell to check.

    Returns:
        bool.
    """
    result = False
    if cell.cell_type == 'code':
        result = re_flags.search(cell.source) is not None
    return result


def get_image_link_re(image_name: str = '') -> re.Pattern:
    """Return regex pattern for image link with given name. If no name - any image link.

    Args:
        image_name (str, optional): Name to find. Defaults to ''.

    Returns:
        re.Pattern: Regex pattern for image link.
    """
    if image_name == '':
        image_name = '.*'
    return re.compile(fr"(\!\[.*\])(\s*\(\s*)(?P<path>{image_name})(\s*\))", re.M)


def correct_output_image_link(image_name: str, image_path, md: str) -> str:
    """Change image link at markdown text from local source to image_path.

    Args:
        image_name (str): Name for image file.
        image_path (_type_): Dir name for images at destination.
        md (str): Markdown text to process.

    Returns:
        str: Text with changed links.
    """
    return re.sub(fr"(\!\[.*\])(\s*\(\s*){image_name}(\s*\))", fr"\1({image_path}/{image_name})", md)


def correct_markdown_image_link(nb: NotebookNode, nb_fn: Path, dest_path: Path, image_path: str):
    """Change image links and copy image at markdown cells at given notebook.

    Args:
        nb (NotebookNode): Jupyter notebook to process.
        nb_fn (Path): Notebook filename.
        dest_path (Path): Destination for converted notebook.
        image_path (str): Path for images at destination.
    """
    re_link = get_image_link_re()
    nb_fn = Path(nb_fn)
    dest_path = Path(dest_path)
    for cell in nb.cells:
        if cell.cell_type == 'markdown':  # look only at markdown cells
            for match in re_link.finditer(cell.source):
                path = match.group('path')
                if not 'http' in path:  # skip external link
                    image_fn = Path(nb_fn).parent / path
                    if image_fn.exists():
                        # path for images
                        dest_images = f"{image_path}/{nb_fn.stem}_files"
                        (dest_path / dest_images).mkdir(exist_ok=True, parents=True)
                        # change link
                        re_path = get_image_link_re(path)
                        cell.source = re_path.sub(fr"\1({dest_images}/{image_fn.name})", cell.source)
                        # copy source
                        copy_name = dest_path / dest_images / image_fn.name
                        shutil.copy(image_fn, copy_name)
                    else:
                        print(f"Image source not exists! filename: {image_fn}")
