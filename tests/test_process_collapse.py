from nbdocs.process import (
    MarkOutputPreprocessor,
    format_output,
    format_output_collapsed,
    md_process_output_flag,
    nb_mark_output,
    OUTPUT_FLAG,
    OUTPUT_FLAG_COLLAPSE,
)

from nbdocs.tests.base import create_nb, test_outputs


def test_nb_mark_output():
    """test mark_output"""
    nb = create_nb(
        code_source="",
        code_outputs=test_outputs,
    )
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_FLAG in outputs[0]["data"]["text/plain"]
    assert OUTPUT_FLAG in outputs[1]["text"]


def test_nb_mark_output_collapse():
    "test mark_output_collapse" ""
    nb = create_nb(
        code_source="#collapse_output\nsome code",
        code_outputs=test_outputs,
    )
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_FLAG_COLLAPSE in outputs[0]["data"]["text/plain"]
    assert OUTPUT_FLAG_COLLAPSE in outputs[1]["text"]
    assert "#collapse_output" not in nb.cells[0].source


def test_MarkOutputPreprocessor():
    """test MarkOutputPreprocessor"""
    processor = MarkOutputPreprocessor()
    processor.enabled = True
    nb = create_nb(
        code_source="",
        code_outputs=test_outputs,
    )
    nb, _ = processor(nb, {})
    outputs = nb.cells[0].outputs
    assert OUTPUT_FLAG in outputs[0]["data"]["text/plain"]
    assert OUTPUT_FLAG in outputs[1]["text"]


def test_md_process_output_flag():
    """test md_process_output_flag"""
    test_md = f"{OUTPUT_FLAG}test text"
    result_md = md_process_output_flag(test_md)
    assert OUTPUT_FLAG not in result_md
    assert format_output in result_md

    test_md = f"{OUTPUT_FLAG_COLLAPSE}test text"
    result_md = md_process_output_flag(test_md)
    assert OUTPUT_FLAG_COLLAPSE not in result_md
    assert format_output_collapsed in result_md
