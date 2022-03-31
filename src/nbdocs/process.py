import re
import shutil
from pathlib import Path
from typing import List

from nbconvert.preprocessors import Preprocessor
from nbformat import NotebookNode

# Flags
# Flag is starts with #, at start of the line, no more symbols at this line except whitespaces.
HIDE = ["hide"]  # hide cell
HIDE_INPUT = ["hide_input"]  # hide code from this cell
HIDE_OUTPUT = ["hide_output"]  # hide output from this cell

HIDE_FLAGS = HIDE + HIDE_INPUT + HIDE_OUTPUT

FLAGS = [] + HIDE_FLAGS  # here will be more flags.


def generate_flags_string(flags: List[str]) -> str:
    """Generate re pattern from list of flags, add flags with '-' instead of '_'.

    Args:
        flags (List[str]): List of flags.

    Returns:
        str: flags, separated by '|'
    """
    result_flags = flags.copy()
    for item in flags:
        if "_" in item:
            result_flags.append(item.replace("_", "-"))
    return "|".join(result_flags)


def get_flags_re(flags: List[str]) -> re.Pattern:
    flag_string = generate_flags_string(flags)
    pattern = rf"^\s*\#\s*({flag_string})\s*$"
    return re.compile(pattern, re.M)


re_flags = get_flags_re(FLAGS)
re_hide = get_flags_re(HIDE)
re_hide_input = get_flags_re(HIDE_INPUT)
re_hide_output = get_flags_re(HIDE_OUTPUT)


def cell_check_flags(cell: NotebookNode) -> bool:
    """Check if cell has nbdocs flags.

    Args:
        cell (NotebookNode): Cell to check.

    Returns:
        bool.
    """
    result = False
    if cell.cell_type == "code":
        result = re_flags.search(cell.source) is not None
    return result


def get_image_link_re(image_name: str = "") -> re.Pattern:
    """Return regex pattern for image link with given name. If no name - any image link.

    Args:
        image_name (str, optional): Name to find. Defaults to ''.

    Returns:
        re.Pattern: Regex pattern for image link.
    """
    if image_name == "":
        image_name = ".*"
    return re.compile(rf"(\!\[.*\])(\s*\(\s*)(?P<path>{image_name})(\s*\))", re.M)


re_link = get_image_link_re()


def correct_output_image_link(image_name: str, image_path, md: str) -> str:
    """Change image link at markdown text from local source to image_path.

    Args:
        image_name (str): Name for image file.
        image_path (_type_): Dir name for images at destination.
        md (str): Markdown text to process.

    Returns:
        str: Text with changed links.
    """
    return re.sub(
        rf"(\!\[.*\])(\s*\(\s*){image_name}(\s*\))",
        rf"\1({image_path}/{image_name})",
        md,
    )


def correct_markdown_image_link(
    nb: NotebookNode, nb_fn: Path, dest_path: Path, image_path: str
):
    """Change image links and copy image at markdown cells at given notebook.

    Args:
        nb (NotebookNode): Jupyter notebook to process.
        nb_fn (Path): Notebook filename.
        dest_path (Path): Destination for converted notebook.
        image_path (str): Path for images at destination.
    """
    nb_fn = Path(nb_fn)
    dest_path = Path(dest_path)
    for cell in nb.cells:
        if cell.cell_type == "markdown":  # look only at markdown cells
            for match in re_link.finditer(cell.source):
                path = match.group("path")
                if "http" not in path:  # skip external link
                    image_fn = Path(nb_fn).parent / path
                    if image_fn.exists():
                        # path for images
                        dest_images = f"{image_path}/{nb_fn.stem}_files"
                        (dest_path / dest_images).mkdir(exist_ok=True, parents=True)
                        # change link
                        re_path = get_image_link_re(path)
                        cell.source = re_path.sub(
                            rf"\1({dest_images}/{image_fn.name})", cell.source
                        )
                        # copy source
                        copy_name = dest_path / dest_images / image_fn.name
                        shutil.copy(image_fn, copy_name)
                    else:
                        print(f"Image source not exists! filename: {image_fn}")


class CorrectMdImageLinkPreprocessor(Preprocessor):
    """
    Change image links and copy image at markdown cells at given notebook.
    """

    def __init__(self, dest_path: Path, image_path: str, **kw):
        super().__init__(**kw)
        self.dest_path = Path(dest_path)
        self.image_path = image_path

    def __call__(self, nb, resources):
        self.nb_fn = nb.filename
        return super().__call__(nb, resources)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "markdown":
            for match in re_link.finditer(cell.source):
                path = match.group("path")
                if "http" not in path:  # skip external link
                    image_fn = Path(self.nb_fn).parent / path
                    if image_fn.exists():
                        # path for images
                        dest_images = f"{self.image_path}/{self.nb_fn.stem}_files"
                        (self.dest_path / dest_images).mkdir(
                            exist_ok=True, parents=True
                        )
                        # change link
                        re_path = get_image_link_re(path)
                        cell.source = re_path.sub(
                            rf"\1({dest_images}/{image_fn.name})", cell.source
                        )
                        # copy source
                        copy_name = self.dest_path / dest_images / image_fn.name
                        shutil.copy(image_fn, copy_name)
                    else:
                        print(f"Image source not exists! filename: {image_fn}")
        return cell, resources


def cell_process_hide_flags(cell: NotebookNode) -> None:
    if re_hide.search(cell.source):
        cell.transient = {"remove_source": True}
        cell.outputs = []
    elif re_hide_input.search(cell.source):
        cell.transient = {"remove_source": True}
    elif re_hide_output.search(cell.source):
        cell.outputs = []
        cell.execution_count = None
        cell.source = re_hide_output.sub(r"", cell.source)


class HideFlagsPreprocessor(Preprocessor):
    """
    Process Hide flags - remove cells, code or output marked by HIDE_FLAGS.
    """

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "code":
            cell_process_hide_flags(cell)
        return cell, resources


def nb_process_hide_flags(nb: NotebookNode) -> None:
    """Process Hide flags - remove cells, code or output marked by HIDE_FLAGS.

    Args:
        nb (NotebookNode): Notebook to process
    """

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell_process_hide_flags(cell)


output_flag = "###output_flag###"


def mark_output(nb: NotebookNode):
    for cell in nb.cells:
        if cell.cell_type == "code":
            for output in cell.outputs:
                if output.get("name", None) == "stdout":
                    output.text = output_flag + output.text


class MarkOutputPreprocessor(Preprocessor):
    """
    Mark outputs at code cells.
    """

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "code":
            for output in cell.outputs:
                if output.get("name", None) == "stdout":
                    output.text = output_flag + output.text
                elif output.get("data") is not None:
                    if "text/plain" in output["data"]:
                        output["data"]["text/plain"] = (
                            output_flag + output["data"]["text/plain"]
                        )
        return cell, resources


def process_output_flag(md: str) -> str:
    return re.sub(r"\s*\#*output_flag\#*", '\n!!! output ""  \n    ', md)
