from nbformat import NotebookNode
from .base import (
    create_cell_metadata,
    create_nb,
    create_nb_metadata,
    create_tmp_image_file,
)


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


def test_create_cell_metadata():
    """create_cell_metadata"""
    nb = create_nb("test code")
    assert nb.cells[0].execution_count is None
    assert not nb.cells[0].metadata
    create_cell_metadata(nb.cells[0])
    assert nb.cells[0].execution_count == 1
    assert nb.cells[0].metadata["test_field"] == "test_value"
    nb = create_nb("test code")
    test_metadata = {"test_meta_field": "test_meta_value"}
    create_cell_metadata(nb.cells[0], metadata=test_metadata, execution_count=2)
    assert nb.cells[0].metadata["test_meta_field"] == "test_meta_value"
    assert nb.cells[0].execution_count == 2
    nb = create_nb("test code")
    nb.cells[0].pop("metadata")
    create_cell_metadata(nb.cells[0])
    assert nb.cells[0].execution_count == 1
    assert nb.cells[0].metadata["test_field"] == "test_value"


def test_create_nb_metadata():
    """test create_nb_metadata"""
    nb = create_nb()
    assert not nb.metadata
    create_nb_metadata(nb)
    assert nb.metadata.language_info == {"name": "python", "version": "3.9"}
    assert nb.metadata.kernelspec == {"language": "python", "name": "python3"}


def test_create_tmp_image_file(tmp_path):
    """test create_tmp_image_file"""
    fn = "test.png"
    create_tmp_image_file(tmp_path / fn)
    assert (tmp_path / fn).exists()
