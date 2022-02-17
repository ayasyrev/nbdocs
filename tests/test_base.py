from pathlib import Path

from nbdocs.core import clean_nb, read_nb
from nbformat import NotebookNode

nb_path = Path('tests/nbs')
nb_filename = nb_path / 'nb_1.ipynb'


def test_read_nb():
    nb = read_nb(nb_filename)
    assert type(nb) == NotebookNode
    assert nb['nbformat']  == 4
    assert nb['cells'][0]['cell_type'] == 'markdown'
    assert nb['cells'][1]['cell_type'] == 'code'
    nb = read_nb(nb_filename, as_version=3)
    assert nb['nbformat']  == 3
