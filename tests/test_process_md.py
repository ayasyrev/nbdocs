from nbdocs.process_md import (
    split_md,
    separate_source_output,
    check_code_cell_empty,
    OUTPUT_CLOSE,
    OUTPUT_OPEN,
    OUTPUT_COLLAPSED,
)


def test_split_md():
    """test split_md"""
    # 2 cells
    input_md = "###cell\nThis is cell 1.\n###cell\nThis is cell 2."
    expected_output = ("This is cell 1.\n", "This is cell 2.")
    output = split_md(input_md)
    assert output == expected_output

    # single cell
    input_md = "###cell\nThis is the only cell."
    expected_output = ("This is the only cell.", )
    output = split_md(input_md)
    assert output == expected_output

    # markdown string without cell flag
    input_md = "This is just a string."
    expected_output = ("This is just a string.", )
    output = split_md(input_md)
    assert output == expected_output


def test_split_md_2():
    """test split_md code cells"""
    # one cell
    text = "###cell\n```python\nSome code\n```"
    result = split_md(text)
    assert result == ("```python\nSome code\n```", )

    # two cells
    text = "###cell\n```python\nSome code\n```###cell\n```python\nMore code\n```"
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


# def test_format_code_cell():
#     """test format_code_cell"""
#     code_open = "```python\n"
#     code_close = "```\n"
#     code = "Some code\n"
#     output = "    output\n"
#     result = format_code_cell(code_open + code + code_close + output)
#     assert result == CELL_SEPARATOR + code_open + code + code_close + EXPECTED_OUTPUT

#     # collapsed
#     result = format_code_cell(code_open + "# collapse_output\n" + code + code_close + output)
#     assert result == CELL_SEPARATOR + code_open + code + code_close + EXPECTED_OUTPUT_COLLAPSED

#     # collapsed, no code
#     result = format_code_cell(code_open + "# collapse_output\n" + code + code_close + output)
#     assert result == CELL_SEPARATOR + code_open + code + code_close + EXPECTED_OUTPUT_COLLAPSED
