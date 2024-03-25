from __future__ import annotations

from .re_tools import re_code_cell_flag, re_code_cell_marker, re_collapse
from .flags import CELL_FLAG, CELL_SEPARATOR


OUTPUT_OPEN = "<details open> <summary>output</summary>  \n"
OUTPUT_COLLAPSED = "<details> <summary>output</summary>  \n"
OUTPUT_CLOSE = "</details>\n"


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


def separate_source_output(cell: str) -> tuple[str, str]:
    """Separate source and output from cell.

    Args:
        cell (str): Markdown cell.

    Returns:
        tuple[str, str]: Source and output.
    """
    blocks = cell.split("```\n")
    output = blocks.pop()
    return "```\n".join(blocks) + "```\n", output


def check_code_cell_empty(code_cell: str) -> bool:
    """Check if code cell is empty.

    Args:
        code_cell (str): Code cell.

    Returns:
        bool: True if code cell is empty.
    """
    lines = tuple(item.strip() for item in re_code_cell_marker.sub("", code_cell).split("\n") if item.strip())
    return len(lines) == 0


def format_code_cell(code_cell: str) -> str:
    """Format code cell: code and output

    Args:
        code_cell (str): Code cell.

    Returns:
        str: Formatted code cell.
    """
    code, output = separate_source_output(code_cell)
    if re_collapse.search(code) is None:
        output_format = OUTPUT_OPEN
    else:
        output_format = OUTPUT_COLLAPSED
        code = re_collapse.sub("", code).lstrip()  # remove flag
    if check_code_cell_empty(code):
        code = ""

    output = output_format + output + OUTPUT_CLOSE
    return CELL_SEPARATOR + code + output


def format_md_cell(md_cell: str) -> str:
    """Format md cell. Now no edits.

    Args:
        md_cell (str): Markdown cell.

    Returns:
        str: Formatted markdown cell.
    """
    return CELL_SEPARATOR + md_cell


def process_md_cells(cells: tuple[str, ...]) -> tuple[str, ...]:
    """Process list of markdown cells.

    Args:
        cells (tuple[str]): List of markdown cells.

    Returns:
        tuple[str]: Processed list of markdown cells.
    """
    return tuple(format_code_cell(cell) if cell.startswith("```") else format_md_cell(cell) for cell in cells)
