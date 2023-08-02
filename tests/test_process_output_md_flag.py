from nbdocs.process import (
    OUTPUT_CODE,
    OUTPUT_CODE_CLOSE,
    OUTPUT_MD,
    OUTPUT_MD_CLOSE,
    md_process_output_flag,
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
    assert res == "<pre>test text</pre>"
    text = "<pre><! -- test text --></pre>"
    res = process_output_md_code_flag(OUTPUT_MD + text + OUTPUT_MD_CLOSE)
    assert res == text
    # if flag not closed -> not working
    text = OUTPUT_MD + "<pre><! -- test text --></pre>"
    res = process_output_md_code_flag(text)
    assert res == text


def test_process_output_code_flag():
    """test process_output_md_flag"""
    CODE_START = "```python\n"
    CODE_END = "\n```"
    text = OUTPUT_CODE + "test text" + OUTPUT_CODE_CLOSE
    res = md_process_output_flag(text)
    assert res == CODE_START + "test text" + CODE_END
    # code inside <pre>
    text = OUTPUT_CODE + "<pre>test text</pre>" + OUTPUT_CODE_CLOSE
    res = md_process_output_flag(text)
    assert res == CODE_START + "test text" + CODE_END

    # if flag not closed -> not working
    text = OUTPUT_CODE + "<pre><! -- test text --></pre>"
    res = md_process_output_flag(text)
    assert res == text
