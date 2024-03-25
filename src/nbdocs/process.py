from __future__ import annotations

from .typing import Cell, CodeCell, MarkdownCell
from .re_tools import re_hide, re_hide_input, re_hide_output, re_output_code, re_code_cell_flag
from .flags import CELL_FLAG, CELL_SEPARATOR


def process_markdown_cell(cell: MarkdownCell) -> MarkdownCell:
    """Process markdown cell.
    Add cell flag.

    Args:
        cell (MarkdownCell): Markdown cell to process.

    Returns:
        MarkdownCell: Processed markdown cell.
    """
    cell.source = f"{CELL_FLAG}\n{cell.source}"
    return cell


def process_code_cell(cell: CodeCell) -> Cell | None:
    """Process cell.
    If source is empty - return None.
    Mark cell, remove source if hide_input, remove output if hide_output.

    Args:
        cell (Cell): Cell to process.

    Returns:
        Cell | None: Processed cell or None.
    """
    if cell.source == "" or re_hide.search(cell.source) is not None:
        return None
    if re_hide_output.search(cell.source) is not None:
        cell.outputs = []
        cell.source = re_output_code.sub(r"", cell.source).lstrip()
    if re_hide_input.search(cell.source) is not None:
        cell.source = CELL_FLAG
        # TODO: check another flags!!!!
    else:
        cell.source = f"{CELL_FLAG}\n{(cell.source)}"
    return cell


def md_process_cell_flag(md: str) -> str:
    """Process cell flag in md.
    Fix splitting of cells - move marker for code cell to beginning.

    Args:
        md (str): Markdown str to process.

    Returns:
        str: Processed markdown str.
    """
    return re_code_cell_flag.sub(r"###cell\n```\1", md)


def split_md(md: str) -> tuple[str, ...]:
    """Split md by cells (marked by CELL_FLAG).
    If no flag - as one cell.

    Args:
        md (str): Markdown str to split.

    Returns:
        list[str]: List of cells as str.
    """
    return tuple(item.strip() for item in md.split(CELL_FLAG) if item.strip())


def format_code_cell(code_cell: str) -> str:
    """Format code cell: code and output

    Args:
        code_cell (str): Code cell.

    Returns:
        str: Formatted code cell.
    """
    return CELL_SEPARATOR + code_cell
