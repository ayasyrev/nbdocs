from pathlib import Path
from typing import List, Tuple, Union

import nbconvert
from nbconvert.exporters.exporter import ResourcesDict
from nbformat import NotebookNode

from nbdocs.core import read_nb
from nbdocs.process import (
    HideFlagsPreprocessor,
    MarkOutputPreprocessor,
    copy_images,
    md_correct_image_link,
    md_find_image_names,
    md_process_output_flag,
)


class MdConverter:
    """MdConverter constructor."""

    def __init__(self) -> None:
        self.md_exporter = nbconvert.MarkdownExporter()
        self.md_exporter.register_preprocessor(HideFlagsPreprocessor, enabled=True)
        self.md_exporter.register_preprocessor(MarkOutputPreprocessor, enabled=True)

    def nb2md(
        self, nb: NotebookNode, resources: ResourcesDict = None
    ) -> Tuple[str, ResourcesDict]:
        """Base convert Nb to Markdown"""
        md, resources = self.md_exporter.from_notebook_node(nb, resources)
        md = md_process_output_flag(md)
        if (image_names := md_find_image_names(md)):
            resources["image_names"] = image_names
        return md, resources

    def __call__(
        self, nb: NotebookNode, resources: ResourcesDict = None
    ) -> Tuple[str, ResourcesDict]:
        """MdConverter call - export given Nb to Md.

        Args:
            nb (NotebookNode): Nb to convert.

        Returns:
            Tuple[str, ResourcesDict]: Md, resources
        """
        return self.nb2md(nb, resources)


def convert2md(
    filenames: Union[Path, List[Path]], dest_path: Path, image_path: str
) -> None:
    """Convert notebooks to markdown.

    Args:
        filenames (List[Path]): List of Nb filenames
        dest_path (Path): Destination for markdown files
        image_path (str): Path for images
    """
    if not isinstance(filenames, list):
        filenames = [filenames]
    md_convertor = MdConverter()
    for nb_fn in filenames:
        nb = read_nb(nb_fn)
        md, resources = md_convertor.nb2md(nb)

        if (image_names := resources["image_names"]):
            dest_images = dest_path / image_path / f"{nb_fn.stem}_files"
            dest_images.mkdir(exist_ok=True, parents=True)

            if len(resources["outputs"]) > 0:
                for image_name, image_data in resources["outputs"].items():
                    md = md_correct_image_link(md, image_name, dest_images)
                    with open(dest_path / dest_images / image_name, "wb") as fh:
                        fh.write(image_data)
                    image_names.discard(image_name)

            done, left = copy_images(image_names, nb_fn.parent, dest_images)
            for name in done:
                md = md_correct_image_link(md, name, dest_images)
            if left:
                print(f"Not fixed image names in nb: {nb_fn}:")
                for fn in left:
                    print(f"   {fn}")

        dest_fn = dest_path / nb_fn.with_suffix(".md").name
        with open(dest_fn, "w", encoding="utf-8") as fh:
            fh.write(md)
