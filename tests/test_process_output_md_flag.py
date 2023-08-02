from nbdocs.process import (
    OUTPUT_MD,
    OUTPUT_MD_CLOSE,
    process_output_md_code_flag,
    remove_spaces,
)


def test_remove_spaces():
    """test remove_spaces"""
    text = "first line\n  second line\n   third line"
    assert remove_spaces(text) == "first line\nsecond line\n third line"
    text = " first line\n  second line\n   third line"
    assert remove_spaces(text) == "first line\n second line\n  third line"


def test_process_output_md_flag():
    """test process_output_md_flag"""
    text = OUTPUT_MD + "test text" + OUTPUT_MD_CLOSE
    res = process_output_md_code_flag(text)
    assert res == "test text"
    text = OUTPUT_MD + "<pre>test text</pre>" + OUTPUT_MD_CLOSE
    res = process_output_md_code_flag(text)
    assert res == "test text"
    text = OUTPUT_MD + "<pre><! -- test text --></pre>" + OUTPUT_MD_CLOSE
    res = process_output_md_code_flag(text)
    assert res == "<! -- test text -->"
    text = OUTPUT_MD + "<pre><! -- test text --></pre>"
    res = process_output_md_code_flag(text)
    assert res == text
