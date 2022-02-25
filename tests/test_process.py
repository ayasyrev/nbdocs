from nbdocs.core import read_nb
from nbdocs.process import cell_check_flags, generate_flags_string, re_flags
from nbdocs.process import get_image_link_re, correct_output_image_link, correct_markdown_image_link

from nbformat import NotebookNode


def test_generate_flags_pattern():
    flags = ['flag1', 'flag2']
    pattern = generate_flags_string(flags)
    assert pattern == 'flag1|flag2'
    flags = ['flag_1', 'flag_2']
    pattern = generate_flags_string(flags)
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


text = '''
Its a dog image.
here - ![dog](images/dog.jpg) ---
=== cat
--- ![cat](images/cat.jpg) ---
just line,
ext link![mkd link] (https://images/some.jpg) dsf
one more line
output link ![jpg](output.jpg) dsf

second output ![jpg] (output2.jpg) dsf
output image, link with whitespaces ![asdf] ( output.jpg ) dsf
'''

text_with_output_image_link = '![jpg](output.jpg)'


def test_get_image_link_re():
    re_link = get_image_link_re()
    all_links = re_link.findall(text)
    assert len(all_links) == 6
    fn = 'output.jpg'
    re_link = get_image_link_re(fn)
    res = re_link.finditer(text)
    assert len(list(res)) == 2
    res = re_link.finditer(text)
    match = next(res)
    assert match.group('path') == fn
    corrected_text = correct_output_image_link(
        image_name='output.jpg',
        image_path='images',
        md=text_with_output_image_link)
    assert corrected_text == '![jpg](images/output.jpg)'
    corrected_text = correct_output_image_link(
        image_name='output2.jpg',
        image_path='images',
        md=text_with_output_image_link)
    assert corrected_text == text_with_output_image_link


new_link_expected = '![dog](images/markdown_image_files/dog.jpg)'
wrong_link = '![dog](images/dogs.jpg)'
external_link = '![dog](https://localhost/dog.jpg)'


def test_correct_markdown_image_link(tmp_path):
    nb_fn = 'tests/test_nbs/markdown_image.ipynb'
    nb = read_nb(nb_fn)
    dest_path = 'test_docs'
    image_path = 'images'
    correct_markdown_image_link(nb, nb_fn, tmp_path / dest_path, image_path)
    assert (tmp_path / dest_path / image_path).exists()
    assert (tmp_path / dest_path / image_path / 'markdown_image_files' / 'dog.jpg').exists()
    assert nb.cells[1].source.splitlines()[1] == new_link_expected
    nb.cells[1].source = external_link
    correct_markdown_image_link(nb, nb_fn, tmp_path / dest_path, image_path)
    assert nb.cells[1].source == external_link
    nb.cells[1].source = wrong_link
    correct_markdown_image_link(nb, nb_fn, tmp_path / dest_path, image_path)
    assert nb.cells[1].source == wrong_link
    nb_fn = 'tests/test_nbs/code_image.ipynb'
    nb = read_nb(nb_fn)
    nb_copy = nb.copy()
    correct_markdown_image_link(nb, nb_fn, tmp_path / dest_path, image_path)
    assert nb == nb_copy
