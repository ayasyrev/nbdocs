from __future__ import annotations

import re
import sys

from .typing import Cell, CodeCell, MarkdownCell

if sys.version_info.minor < 9:  # pragma: no cover
    from typing import Pattern

    rePattern = Pattern[str]
else:
    rePattern = re.Pattern[str]

# Flags
# Flag is starts with #, at start of the line, no more symbols at this line except whitespaces.
HIDE = ["hide"]  # hide cell
HIDE_INPUT = ["hide_input"]  # hide code from this cell
HIDE_OUTPUT = ["hide_output"]  # hide output from this cell

HIDE_FLAGS = HIDE + HIDE_INPUT + HIDE_OUTPUT

FLAGS: list[str] = [] + HIDE_FLAGS  # here will be more flags.

COLLAPSE_OUTPUT = "collapse_output"

CELL_FLAG = "###cell"
CELL_SEPARATOR = "<!-- cell -->\n"  # In result md marks cells by this separator


def generate_flags_string(flags: list[str]) -> str:
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


def get_flags_re(flags: list[str]) -> rePattern:
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
re_collapse = get_flags_re([COLLAPSE_OUTPUT])
re_output_code = get_flags_re(["output_code"])
re_code_cell_flag = re.compile(r"^```(\w*\s*)\n###cell", re.M)


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


def format_md_cell(md_cell: str) -> str:
    """Format md cell. Now no editions

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
