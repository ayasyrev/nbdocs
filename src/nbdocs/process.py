import re
import shutil
from pathlib import Path
from typing import List, Set, Tuple

from nbconvert.exporters.exporter import ResourcesDict
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
    """Create Regex pattern from list of flags.

    Args:
        flags (List[str]): List of flags.

    Returns:
        re.Pattern: Regex pattern.
    """
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


def md_find_image_names(md: str) -> Set[str]:
    """Return set of image name from internal mage links

    Args:
        md (str): Markdown str to find names.

    Returns:
        Set[str]: Set of image names
    """
    re_link = get_image_link_re()
    return set(
        path
        for match in re_link.finditer(md)
        if "http" not in (path := match.group("path"))
    )


def md_correct_image_link(md: str, image_name: str, image_path: str) -> str:
    """Change image link at markdown text from local source to image_path.

    Args:
        md (str): Markdown text to process.
        image_name (str): Name for image file.
        image_path (str): Dir name for images at destination.

    Returns:
        str: Text with changed links.
    """
    return re.sub(
        rf"(\!\[.*\])(\s*\(\s*){image_name}(\s*\))",
        rf"\1({image_path}/{image_name})",
        md,
    )


def copy_images(
    image_names: List, source: Path, dest: Path
) -> Tuple[List[str], List[str]]:
    """Copy images from source to dest. Return list of copied and list of left.

    Args:
        image_names (List): List of names
        source (Path): PAth of source dir (parent)
        dest (Path): Destination path

    Returns:
        Tuple[List[str], List[str]]: _description_
    """
    image_names = set(image_names)
    done = []
    files_to_copy = [
        Path(image_name) for image_name in image_names if (source / image_name).exists()
    ]
    if len(files_to_copy) > 0:
        dest.mkdir(exist_ok=True, parents=True)
        for fn in files_to_copy:
            shutil.copy(source / fn, dest / fn.name)
            done.append(str(fn))
    image_names.difference_update(done)
    return done, image_names


# check relative link (../../), ? can we correct links after converting
def cell_md_correct_image_link(
    cell: NotebookNode, nb_fn: Path, dest_path: Path, image_path: str
) -> None:
    """Change image links at given markdown cell and copy linked image to image path at dest.

    Args:
        cell (NotebookNode): _description_
    """
    image_names = md_find_image_names(cell.source)
    for image_name in image_names:
        image_fn = Path(nb_fn).parent / image_name  # check relative path in link
        if image_fn.exists():
            # path for images
            dest_images = f"{image_path}/{nb_fn.stem}_files"
            (dest_path / dest_images).mkdir(exist_ok=True, parents=True)
            # change link
            re_path = get_image_link_re(image_name)
            cell.source = re_path.sub(
                rf"\1({dest_images}/{image_fn.name})", cell.source
            )
            # copy source
            copy_name = dest_path / dest_images / image_fn.name
            shutil.copy(image_fn, copy_name)
        else:
            print(f"Image source not exists! filename: {image_fn}")


def correct_markdown_image_link(
    nb: NotebookNode, nb_fn: Path, dest_path: Path, image_path: str
):
    """Change image links at markdown cells and copy linked image to image path at dest.

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
            cell_md_correct_image_link(cell, nb_fn, dest_path, image_path)


class CorrectMdImageLinkPreprocessor(Preprocessor):
    """
    Change image links and copy image at markdown cells at given notebook.
    """

    def __init__(self, dest_path: Path, image_path: str, **kw):
        super().__init__(**kw)
        self.dest_path = Path(dest_path)
        self.image_path = image_path
        self.nb_fn = None

    def __call__(
        self, nb: NotebookNode, resources: ResourcesDict
    ) -> Tuple[NotebookNode, ResourcesDict]:
        self.nb_fn = Path(nb.get("filename", "."))
        return super().__call__(nb, resources)

    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "markdown":
            cell_md_correct_image_link(
                cell, self.nb_fn, self.dest_path, self.image_path
            )
        return cell, resources


def cell_process_hide_flags(cell: NotebookNode) -> None:
    """Process cell - remove input, output or both.

    Args:
        cell (NotebookNode): Notebook cell
    """
    if re_hide.search(cell.source):
        cell.transient = {"remove_source": True}
        cell.source = ""
        cell.outputs = []
    elif re_hide_input.search(cell.source):
        cell.transient = {"remove_source": True}
        cell.source = ""
    elif re_hide_output.search(cell.source):
        cell.outputs = []
        cell.execution_count = None
        cell.source = re_hide_output.sub(r"", cell.source)


class HideFlagsPreprocessor(Preprocessor):
    """
    Process Hide flags - remove cells, code or output marked by HIDE_FLAGS.
    """

    def preprocess_cell(self, cell, resources, index):
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
# format_output = '\n!!! output ""  \n    '
format_output = '\n??? done "output"  \n    <pre>'


def mark_output(outputs: List[NotebookNode]) -> None:
    """Mark text at outputs by flag.

    Args:
        outputs (List[NotebookNode]): Cell outputs.
    """
    for output in outputs:
        if output.get("name", None) == "stdout":
            output.text = output_flag + output.text
        elif output.get("data") is not None:
            if "text/plain" in output["data"]:
                output["data"]["text/plain"] = (
                    output_flag + output["data"]["text/plain"]
                )


def nb_mark_output(nb: NotebookNode):
    """Mark cells with output.
    Better use Preprocessor version

    Args:
        nb (NotebookNode): _description_
    """
    for cell in nb.cells:
        if cell.cell_type == "code":
            mark_output(cell.outputs)


class MarkOutputPreprocessor(Preprocessor):
    """
    Mark outputs at code cells.
    """

    def preprocess_cell(self, cell, resources, index):
        """
        Apply a transformation on each cell. See base.py for details.
        """
        if cell.cell_type == "code":
            mark_output(cell.outputs)

        return cell, resources


def md_process_output_flag(md: str) -> str:
    """Reformat marked output.

    Args:
        md (str): Markdown string

    Returns:
        str: Markdown string.
    """
    return re.sub(r"\s*\#*output_flag\#*", format_output, md)
