from nbformat import NotebookNode
from .base import create_nb


def test_create_nb():
    """test for create_nb"""
    # empty nb
    nb = create_nb()
    assert isinstance(nb, NotebookNode)
    assert len(nb.cells) == 0
    # only code cell
    nb = create_nb("test code")
    assert len(nb.cells) == 1
    assert nb.cells[0]["cell_type"] == "code"
    assert nb.cells[0].source == "test code"
    # only md cell
    nb = create_nb(md_source="test md")
    assert len(nb.cells) == 1
    assert nb.cells[0]["cell_type"] == "markdown"
    assert nb.cells[0].source == "test md"
    # code and markdown
    nb = create_nb(code_source="test code", md_source="test md")
    assert len(nb.cells) == 2
    assert nb.cells[0]["cell_type"] == "code"
    assert nb.cells[0].source == "test code"
    assert nb.cells[1]["cell_type"] == "markdown"
    assert nb.cells[1].source == "test md"
