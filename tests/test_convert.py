from nbdocs.convert import MdConverter

from .base import create_nb


def test_MdConverter(tmp_path):
    """ test for MdConverter"""
    md_converter = MdConverter(tmp_path, "images")
    nb = create_nb()
    md, resources = md_converter(nb)
