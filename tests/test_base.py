from pathlib import Path

import nbformat
from nbdocs.core import (cell_check_flags, clean_nb, generate_flags_pattern,
                         re_flags, read_nb)
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


def test_generate_flags_pattern():
    flags = ['flag1', 'flag2']
    pattern = generate_flags_pattern(flags)
    assert pattern == 'flag1|flag2'
    flags = ['flag_1', 'flag_2']
    pattern = generate_flags_pattern(flags)
    assert 'flag-1' in pattern
    assert 'flag-2' in pattern


def test_re_flags():
    assert re_flags.search('hide') is None
    assert re_flags.search('hide\n #hide') is not None


def test_cell_check_flags():

    cell = NotebookNode(cell_type='markdown', source='markdown cell.')
    assert not cell_check_flags(cell)

    cell['cell_type'] = 'code'
    cell['source'] = '# hide'
    assert cell_check_flags(cell)

    cell['source'] = '# do hide'
    assert not cell_check_flags(cell)

    cell['source'] = 'aaa # hide'
    assert not cell_check_flags(cell)

    cell['cell_type'] = 'markdown'
    assert not cell_check_flags(cell)
