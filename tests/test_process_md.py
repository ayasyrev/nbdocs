from nbdocs.process import (
    md_process_cell_flag,
    re_code_cell_flag,
)


def test_md_process_cell_flag():
    """test md_process_cell_flag"""
    # code cell
    text = "```\n###cell\nSome code\n```"
    result = md_process_cell_flag(text)
    assert result == "###cell\n```\nSome code\n```"

    # assert re_code_cell_flag.search(text) is not None
    # result = re_code_cell_flag.sub(r"###cell\n```", text)
    # assert result == "###cell\n```\nSome code\n```"

    text = "```python\n###cell\nSome code\n```"
    result = md_process_cell_flag(text)
    assert result == "###cell\n```python\nSome code\n```"

    text = "\n```python \n###cell\nSome code\n```"
    result = md_process_cell_flag(text)
    assert result == "\n###cell\n```python \nSome code\n```"
