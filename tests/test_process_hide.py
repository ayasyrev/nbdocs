from nbconvert.exporters.exporter import ResourcesDict
from nbdocs.process import HideFlagsPreprocessor, nb_process_hide_flags
from nbdocs.tests.base import create_nb


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
    assert cell.metadata["transient"] == {"remove_source": True}
    # hide input
    source = "# hide_input\n some code"
    nb = create_nb(source)
    nb, resources = processor(nb, resources)
    cell = nb.cells[0]
    assert len(cell.outputs) == 3
    assert cell.metadata["transient"] == {"remove_source": True}
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
    assert cell.metadata["transient"] == {"remove_source": True}
    # hide input
    source = "# hide_input\n some code"
    nb = create_nb(source)
    nb_process_hide_flags(nb)
    cell = nb.cells[0]
    assert len(cell.outputs) == 3
    assert cell.metadata["transient"] == {"remove_source": True}
    # hide output
    source = "# hide_output\n some code"
    nb = create_nb(source)
    nb_process_hide_flags(nb)
    cell = nb.cells[0]
    assert len(cell.outputs) == 0
    assert "some code" in cell.source
    assert "hide_input" not in cell.source
