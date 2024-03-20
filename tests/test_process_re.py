from nbformat import NotebookNode

from nbdocs.process import (
    cell_check_flags,
    generate_flags_string,
    re_flags,
    re_hide,
    re_hide_input,
    re_hide_output,
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


def test_cell_check_flags():
    """check flags"""
    cell = NotebookNode(cell_type="markdown", source="markdown cell.")
    assert not cell_check_flags(cell)

    cell["cell_type"] = "code"
    cell["source"] = "# hide"
    assert cell_check_flags(cell)

    cell["source"] = "# do hide"
    assert not cell_check_flags(cell)

    cell["source"] = "aaa # hide"
    assert not cell_check_flags(cell)

    cell["cell_type"] = "markdown"
    assert not cell_check_flags(cell)


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
