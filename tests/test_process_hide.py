from nbconvert.exporters.exporter import ResourcesDict

from nbdocs.process import (
    HideFlagsPreprocessor,
    MarkOutputPreprocessor,
    format_output,
    md_process_output_flag,
    nb_mark_output,
    nb_process_hide_flags,
    output_flag,
)
from tests.base import create_nb


def test_HideFlagsPreprocessor():
    """test for HideFlagsPreprocessor"""
    processor = HideFlagsPreprocessor()
    processor.enabled = True
    resources = ResourcesDict()
    # hide
    source = "# hide"
    nb = create_nb(source)
    nb, resources = processor(nb, resources)
    cell = nb.cells[0]
    assert len(cell.outputs) == 0
    assert cell.transient == {"remove_source": True}
    # hide input
    source = "# hide_input\n some code"
    nb = create_nb(source)
    nb, resources = processor(nb, resources)
    cell = nb.cells[0]
    assert len(cell.outputs) == 3
    assert cell.transient == {"remove_source": True}
    # hide output
    source = "# hide_output\n some code"
    nb = create_nb(source)
    nb, resources = processor(nb, resources)
    cell = nb.cells[0]
    assert len(cell.outputs) == 0
    assert "some code" in cell.source
    assert "hide_input" not in cell.source


def test_nb_process_hide_flags():
    """test for nb_process_hide_flags"""
    # hide
    source = "# hide"
    nb = create_nb(source)
    nb_process_hide_flags(nb)
    cell = nb.cells[0]
    assert len(cell.outputs) == 0
    assert cell.transient == {"remove_source": True}
    # hide input
    source = "# hide_input\n some code"
    nb = create_nb(source)
    nb_process_hide_flags(nb)
    cell = nb.cells[0]
    assert len(cell.outputs) == 3
    assert cell.transient == {"remove_source": True}
    # hide output
    source = "# hide_output\n some code"
    nb = create_nb(source)
    nb_process_hide_flags(nb)
    cell = nb.cells[0]
    assert len(cell.outputs) == 0
    assert "some code" in cell.source
    assert "hide_input" not in cell.source


def test_nb_mark_output():
    """test nb_mark_output"""
    nb = create_nb("")
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert "###output_flag###" in outputs[0]["data"]["text/plain"]
    assert "###output_flag###" in outputs[1]["text"]


def test_MarkOutputPreprocessor():
    """test MarkOutputPreprocessor"""
    processor = MarkOutputPreprocessor()
    processor.enabled = True
    nb = create_nb("")
    nb, _ = processor(nb, {})
    outputs = nb.cells[0].outputs
    assert "###output_flag###" in outputs[0]["data"]["text/plain"]
    assert "###output_flag###" in outputs[1]["text"]


def test_md_process_output_flag():
    """test md_process_output_flag"""
    test_md = f"{output_flag}test text"
    result_md = md_process_output_flag(test_md)
    assert output_flag not in result_md
    assert format_output in result_md
