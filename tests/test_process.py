from nbdocs.process import split_md


def test_split_md():
    """test split_md"""
    # 2 cells
    input_md = "###cell\nThis is cell 1.\n\n###cell\nThis is cell 2."
    expected_output = ("This is cell 1.", "This is cell 2.")
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
