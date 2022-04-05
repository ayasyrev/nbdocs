from pathlib import Path
from typing import List, Tuple

import nbconvert
from nbconvert.exporters.exporter import ResourcesDict
from nbformat import NotebookNode

from nbdocs.core import read_nb
from nbdocs.process import (
    CorrectMdImageLinkPreprocessor,
    HideFlagsPreprocessor,
    MarkOutputPreprocessor,
    correct_output_image_link,
    md_process_output_flag,
)


class MdConverter:
    """MdConverter constructor.
    """
    def __init__(self, dest_path: Path, image_path: str) -> None:
        self.md_exporter = nbconvert.MarkdownExporter()
        self.md_exporter.register_preprocessor(HideFlagsPreprocessor, enabled=True)
        self.md_exporter.register_preprocessor(MarkOutputPreprocessor, enabled=True)
        correct_image_link_preprocessor = CorrectMdImageLinkPreprocessor(
            dest_path, image_path
        )
        self.md_exporter.register_preprocessor(correct_image_link_preprocessor, enabled=True)

    def __call__(self, nb: NotebookNode) -> Tuple[str, ResourcesDict]:
        md, resources = self.md_exporter.from_notebook_node(nb)
        md = md_process_output_flag(md)
        return md, resources


def convert2md(filenames: List[Path], dest_path: Path, image_path: str) -> None:
    """Convert notebooks to markdown.

    Args:
        filenames (List[Path]): List of Nb filenames
        dest_path (Path): Destination for markdown files
        image_path (str): Path for images
    """
    md_convertor = MdConverter(dest_path, image_path)
    for nb_fn in filenames:
        nb = read_nb(nb_fn)
        md, resources = md_convertor(nb)

        dest_fn = dest_path / nb_fn.with_suffix(".md").name

        if len(resources["outputs"]) > 0:
            dest_images = f"{image_path}/{nb_fn.stem}_files"
            (dest_path / dest_images).mkdir(exist_ok=True)
            for image_name, image_data in resources["outputs"].items():
                md = correct_output_image_link(image_name, dest_images, md)
                with open(
                    dest_path / dest_images / image_name, "wb"
                ) as fh:
                    fh.write(image_data)

        with open(dest_fn, "w", encoding="utf-8") as fh:
            fh.write(md)
