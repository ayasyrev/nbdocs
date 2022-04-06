from nbdocs.core import write_nb
from nbdocs.convert import MdConverter, convert2md

from .base import create_nb, create_tmp_image_file


def test_MdConverter():
    """test for MdConverter"""
    md_converter = MdConverter()
    # md cell
    nb = create_nb(md_source="test_md")
    md, resources = md_converter.nb2md(nb)
    assert md == "test_md\n"
    assert resources["output_extension"] == ".md"
    assert not resources["image_names"]
    # code cell
    nb = create_nb("test_code")
    md, resources = md_converter.nb2md(nb)
    assert "test_code" in md
    assert "![png](output_0_2.png)" in md
    assert resources["outputs"] == {"output_0_2.png": b"g"}
    assert "output_0_2.png" in resources["image_names"]
    # code and markdown, call()
    nb = create_nb("test_code", md_source="![cat](cat.jpg)")
    md, resources = md_converter(nb)
    assert "test_code" in md
    assert "![png](output_0_2.png)" in md
    assert resources["outputs"] == {"output_0_2.png": b"g"}
    assert "output_0_2.png" in resources["image_names"]
    assert "cat.jpg" in resources["image_names"]


def test_convert2md(tmp_path, capsys):
    """test convert2md"""
    image_name = "t_1.png"
    create_tmp_image_file(tmp_path / image_name)
    dest = tmp_path / "dest"
    nb = create_nb(
        code_source="test_code",
        md_source=f"![test image]({image_name})\n![wrong name](wrong_name.png)")
    nb_name = "test_nb.ipynb"
    write_nb(nb, tmp_path / nb_name)

    convert2md(tmp_path / nb_name, dest, "images")
    with open(
        (tmp_path / dest / nb_name).with_suffix(".md"), "r", encoding="utf-8"
    ) as fh:
        md = fh.read()
    assert "test_code" in md
    dest_images = dest / "images" / "test_nb_files"
    assert dest_images.exists()
    assert (dest_images / image_name).exists()
    assert (dest_images / "output_0_2.png").exists()
    captured = capsys.readouterr()
    assert "Not fixed image names in nb:" in captured.out
    assert "wrong_name.png" in captured.out
