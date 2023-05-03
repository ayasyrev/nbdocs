from pathlib import Path

from nbdocs.clean import clean_nb, clean_nb_file
from nbdocs.core import read_nb, write_nb
from nbdocs.tests.base import (
    create_cell_metadata,
    create_nb,
    create_nb_metadata,
    test_outputs,
)

nb_metadata = {
    "language_info": {"name": "python", "version": "3.9"},
    "kernelspec": {"language": "python", "name": "python3"},
}
code_metadata = {
    "test_field": "test_value",
    "executeTime": dict([("end_time", "09:31:50"), ("start_time", "09:31:49")]),
}


def test_clean_nb():
    """test clean_nb"""
    nb = create_nb(
        code_source="test code",
        code_outputs=test_outputs,
    )
    create_nb_metadata(nb, nb_metadata)
    create_cell_metadata(nb.cells[0], code_metadata)
    assert nb.metadata
    assert nb.cells[0].metadata
    clean_nb(nb, clear_execution_count=False)
    assert nb.metadata == {"language_info": {"name": "python"}}
    assert nb.cells[0].execution_count == 1
    assert nb.cells[0].outputs[0].execution_count == 1
    assert not nb.cells[0].metadata
    clean_nb(nb)
    assert not nb.cells[0].execution_count
    assert not nb.cells[0].outputs[0].execution_count


def test_clean_nb_file(tmp_path: Path):
    """test clean_nb_file"""
    test_nb_fn = tmp_path / "test_nb.ipynb"
    nb = create_nb(
        code_source="test code",
        code_outputs=test_outputs,
    )
    create_nb_metadata(nb, nb_metadata)
    create_cell_metadata(nb.cells[0], code_metadata)
    write_nb(nb, test_nb_fn)

    clean_nb_file(test_nb_fn)
    nb_cleared = read_nb(test_nb_fn)
    assert nb_cleared.metadata == {"language_info": {"name": "python"}}
    assert not nb_cleared.cells[0].execution_count
    assert not nb_cleared.cells[0].outputs[0].execution_count
    assert not nb_cleared.cells[0].metadata
