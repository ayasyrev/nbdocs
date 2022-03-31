from pathlib import Path
from typing import List

import nbconvert

from nbdocs.core import read_nb
from nbdocs.process import (
    CorrectMdImageLinkPreprocessor,
    HideFlagsPreprocessor,
    MarkOutputPreprocessor,
    correct_output_image_link,
    process_output_flag,
)


def convert2md(filenames: List[Path], dest_path: Path, image_path: str):
    md_exporter = nbconvert.MarkdownExporter()
    md_exporter.register_preprocessor(HideFlagsPreprocessor, enabled=True)
    md_exporter.register_preprocessor(MarkOutputPreprocessor, enabled=True)
    correct_image_link_preprocessor = CorrectMdImageLinkPreprocessor(
        dest_path, image_path
    )
    md_exporter.register_preprocessor(correct_image_link_preprocessor, enabled=True)
    for nb_fn in filenames:
        nb = read_nb(nb_fn)
        (md, resources) = md_exporter.from_notebook_node(nb)
        md = process_output_flag(md)

        dest_fn = dest_path / nb_fn.with_suffix(".md").name

        if len(resources["outputs"]) > 0:
            dest_images = f"{image_path}/{nb_fn.stem}_files"
            (dest_path / dest_images).mkdir(exist_ok=True)
            for image_name, image_data in resources["outputs"].items():
                with open(dest_path / dest_images / image_name, "wb") as f:
                    md = correct_output_image_link(image_name, dest_images, md)
                    f.write(image_data)

        with open(dest_fn, "w") as f:
            f.write(md)
