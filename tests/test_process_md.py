from nbdocs.process_md import (
    md_process_cell_flag,
    split_md,
    separate_source_output,
    check_code_cell_empty,
    format_code_cell,
    OUTPUT_CLOSE,
    OUTPUT_OPEN,
    OUTPUT_COLLAPSED,
)
from nbdocs.flags import CELL_SEPARATOR


def test_md_process_cell_flag():
    """test md_process_cell_flag"""
    # code cell
    text = "```\n###cell\nSome code\n```"
    result = md_process_cell_flag(text)
    assert result == "###cell\n```\nSome code\n```"

    text = "```python\n###cell\nSome code\n```"
    result = md_process_cell_flag(text)
    assert result == "###cell\n```python\nSome code\n```"

    text = "\n```python \n###cell\nSome code\n```"
    result = md_process_cell_flag(text)
    assert result == "\n###cell\n```python \nSome code\n```"


def test_split_md():
    """test split_md"""
    # one cell
    text = "###cell\n```python\nSome code\n```"
    result = split_md(text)
    assert result == ("```python\nSome code\n```", )

    # two cells
    text = "###cell\n```python\nSome code\n```\n\n###cell\n```python\nMore code\n```"
    result = split_md(text)
    assert result == ("```python\nSome code\n```", "```python\nMore code\n```")


def test_separate_source_output():
    """test separate_source_output"""
    cell = "```python\nSome code\n```\n    output\n"
    code, output = separate_source_output(cell)
    assert code == "```python\nSome code\n```\n"
    assert output == "    output\n"

    cell = "```\nSome code\n```\n    output\n"
    code, output = separate_source_output(cell)
    assert code == "```\nSome code\n```\n"
    assert output == "    output\n"


def test_check_code_cell_empty():
    """test check_code_cell_empty"""
    assert check_code_cell_empty("```\n```\n")
    assert check_code_cell_empty("```\n\n```\n")
    assert not check_code_cell_empty("```python\nSome code\n```")


EXPECTED_OUTPUT = OUTPUT_OPEN + "    output\n" + OUTPUT_CLOSE
EXPECTED_OUTPUT_COLLAPSED = OUTPUT_COLLAPSED + "    output\n" + OUTPUT_CLOSE


def test_format_code_cell():
    """test format_code_cell"""
    code_open = "```python\n"
    code_close = "```\n"
    code = "Some code\n"
    output = "    output\n"
    result = format_code_cell(code_open + code + code_close + output)
    assert result == CELL_SEPARATOR + code_open + code + code_close + EXPECTED_OUTPUT

    # collapsed
    result = format_code_cell(code_open + "# collapse_output\n" + code + code_close + output)
    assert result == CELL_SEPARATOR + code_open + code + code_close + EXPECTED_OUTPUT_COLLAPSED

    # collapsed, no code
    result = format_code_cell(code_open + "# collapse_output\n" + code + code_close + output)
    assert result == CELL_SEPARATOR + code_open + code + code_close + EXPECTED_OUTPUT_COLLAPSED
