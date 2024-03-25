from __future__ import annotations

from pathlib import Path
from typing import Any

import nbconvert
from nbformat import v4 as nbformat

from rich.progress import track

from .cfg_tools import NbDocsCfg
from .core import read_nb
from .process_cell import (
    process_code_cell,
    process_markdown_cell,
)

from .typing import Nb


class MdConverter:
    """MdConverter constructor."""

    cell_preprocessor = {
        "markdown": process_markdown_cell,
        "code": process_code_cell,
    }

    def __init__(self) -> None:
        self.md_exporter = nbconvert.MarkdownExporter()

    def export2md(self, nb: Nb) -> tuple[str, dict[str, Any]]:
        """Export given Nb to Markdown with default exporter.

        Args:
            nb (Notebook): Nb to convert.

        Returns:
            Tuple[str, ResourcesDict]: Md, resources
        """
        return self.md_exporter.from_notebook_node(nb)

    def preprocess_nb(self, nb: Nb) -> Nb:
        """Preprocess notebook.
        Remove empty cells, hide marked cells, source, output.
        Return nb with processed cells, cells separated by new md cells with comments.

        Args:
            nb (Nb): Notebook to process.

        Returns:
            Nb: Processed notebook.
        """
        result = []
        for num_cell, cell in enumerate(nb.cells):
            if (processed_cell := self.cell_preprocessor[cell.cell_type](cell)) is not None:
                cell_comment = nbformat.new_markdown_cell(f"###cell\n<!-- cell #{num_cell} {cell.cell_type} -->")
                result.extend([cell_comment, processed_cell])
        nb.cells = result
        return nb

    def nb2md(self, nb: Nb) -> tuple[tuple[str, ...], dict[str, Any]]:
        """Base convert Nb to Markdown. Preprocess notebook and export to Markdown."""
        nb = self.preprocess_nb(nb)
        md, resources = self.export2md(nb)
        md_cells = tuple(item for item in md.split("###cell\n") if item)
        return md_cells, resources


def convert2md(filenames: Path | list[Path], cfg: NbDocsCfg) -> None:
    """Convert notebooks to markdown.

    Args:
        filenames (List[Path]): List of Nb filenames
        cfg (NbDocsCfg): NbDocsCfg
    """
    if not isinstance(filenames, list):
        filenames = [filenames]
    docs_path = Path(cfg.docs_path)
    docs_path.mkdir(exist_ok=True, parents=True)
    converter = MdConverter()
    for nb_fn in track(filenames):
        nb = read_nb(nb_fn)
        md, _resources = converter.nb2md(nb)
        with open(Path(cfg.docs_path) / nb_fn.with_suffix(".md").name, "w", encoding="utf-8") as fh:
            fh.write(md)


def nb_newer(nb_name: Path, docs_path: Path) -> bool:
    """return True if nb_name is newer than docs_path."""
    md_name = (docs_path / nb_name.name).with_suffix(".md")
    return not md_name.exists() or nb_name.stat().st_mtime > md_name.stat().st_mtime


def filter_changed(nb_names: list[Path], cfg: NbDocsCfg) -> list[Path]:
    """Filter list of Nb to changed only (compare modification date with dest name).

    Args:
        nb_names (List[Path]): List of Nb filenames.
        dest (Path, optional): Destination folder for md files.
            If not given default from settings. Defaults to None.

    Returns:
        List[Path]: List of Nb filename with newer modification time.
    """
    docs_path = Path(cfg.docs_path)
    return [nb_name for nb_name in nb_names if nb_newer(nb_name, docs_path)]
