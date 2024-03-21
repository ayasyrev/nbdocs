from nbdocs.process import (
    generate_flags_string,
    re_flags,
    re_hide,
    re_hide_input,
    re_hide_output,
    re_code_cell_flag,
)


def test_generate_flags_string():
    """Generate pattern for flags"""
    flags = ["flag1", "flag2"]
    pattern = generate_flags_string(flags)
    assert pattern == "flag1|flag2"
    flags = ["flag_1", "flag_2"]
    pattern = generate_flags_string(flags)
    assert "flag-1" in pattern
    assert "flag-2" in pattern


def test_re_flags():
    """test search"""
    assert re_flags.search("hide") is None
    assert re_flags.search("hide\n #hide") is not None


def test_predefined_patterns():
    """test predefined patterns"""
    assert re_hide.search("# hide") is not None
    assert re_hide.search("#hide") is not None
    assert re_hide.search("# hide_input") is None

    assert re_hide_input.search("# hide_input") is not None
    assert re_hide_input.search("#hide_input") is not None
    assert re_hide_input.search("# hide") is None

    assert re_hide_output.search("# hide_output") is not None
    assert re_hide_output.search("#hide_output") is not None
    assert re_hide_output.search("# hide") is None
    assert re_hide_output.search("# hide_input") is None

    text = "#hide_output\nSome text"
    assert re_hide_output.sub(r"", text).lstrip() == "Some text"


def test_re_code_cell_flag():
    """test re_code_cell_flag"""
    # code cell
    text = "```\n###cell\nSome code\n```"
    assert re_code_cell_flag.search(text) is not None
    result = re_code_cell_flag.sub(r"###cell\n```", text)
    assert result == "###cell\n```\nSome code\n```"

    text = "```python\n###cell\nSome code\n```"
    assert re_code_cell_flag.search(text) is not None
    result = re_code_cell_flag.sub(r"###cell\n```\1", text)
    assert result == "###cell\n```python\nSome code\n```"

    text = "```python \n###cell\nSome code\n```"
    assert re_code_cell_flag.search(text) is not None
    result = re_code_cell_flag.sub(r"###cell\n```\1", text)
    assert result == "###cell\n```python \nSome code\n```"

    text = "\n```python \n###cell\nSome code\n```"
    assert re_code_cell_flag.search(text) is not None
    result = re_code_cell_flag.sub(r"###cell\n```\1", text)
    # assert result == "###cell\n```python \nSome code\n```"
