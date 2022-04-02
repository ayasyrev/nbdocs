from nbformat import NotebookNode, v4 as nbformat


def create_code_cell(source: str) -> NotebookNode:
    """Create basic code cell with given source.
    Outputs basic text data.

    Args:
        source (str): Source for code cell

    Returns:
        NotebookNode: Nb code cell.
    """
    outputs = [
        nbformat.new_output("display_data", data={"text/plain": "b"}),
        nbformat.new_output("stream", name="stdout", text="a"),
        nbformat.new_output("display_data", data={"image/png": "Zw=="}),
    ]
    return nbformat.new_code_cell(source=source, outputs=outputs)


def create_markdown_cell(source: str) -> NotebookNode:
    """Create basic markdown cell with given source.

    Args:
        source (str): Source ror markdown cell

    Returns:
        NotebookNode: Nb markdown cell.
    """
    return nbformat.new_markdown_cell(source)


def create_nb(code_source: str = None, md_source: str = None) -> NotebookNode:
    """Create basic test nb.

    Args:
        code_source (str, optional): Source for code cell. Defaults to None.
        md_source (_type_, optional): Source for markdown cell. Defaults to None.

    Returns:
        NotebookNode: Nb for test
    """
    cells = []
    if code_source is not None:
        cells.append(create_code_cell(code_source))
    if md_source is not None:
        cells.append(create_markdown_cell(md_source))
    return nbformat.new_notebook(cells=cells)
