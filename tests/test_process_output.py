from nbdocs.process import (
    OUTPUT_CODE,
    OUTPUT_CODE_CLOSE,
    MarkOutputPreprocessor,
    format_output,
    format_output_collapsed,
    md_process_output_flag,
    nb_mark_output,
    OUTPUT_FLAG,
    OUTPUT_FLAG_COLLAPSE,
    OUTPUT_MD,
    OUTPUT_MD_CLOSE,
    nb_process_hide_flags,
)

from nbdocs.tests.base import create_test_nb


def test_nb_mark_output():
    """test mark_output"""
    nb = create_test_nb(code_source="some code")
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_FLAG in outputs[0]["data"]["text/plain"]
    assert outputs[0]["data"]["text/plain"].startswith(f"{OUTPUT_FLAG}<pre>")
    assert OUTPUT_FLAG not in outputs[1]["text"]


def test_nb_mark_output_md():
    """test mark_output md - if no source - OUTPUT_MD"""
    nb = create_test_nb(code_source="")
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_MD in outputs[0]["data"]["text/plain"]
    assert "<pre>" in outputs[0]["data"]["text/plain"]
    assert OUTPUT_MD_CLOSE in outputs[1]["text"]
    assert "<pre>" in outputs[1]["text"]

    # source marked as hide
    nb = create_test_nb(code_source="# hide_input\nsome code")
    nb_process_hide_flags(nb)
    assert nb.cells[0].source == ""
    assert nb.cells[0].metadata.get("output_type", "") == ""
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_MD in outputs[0]["data"]["text/plain"]
    assert "<pre>" in outputs[0]["data"]["text/plain"]
    assert OUTPUT_MD_CLOSE in outputs[1]["text"]
    assert "<pre>" in outputs[1]["text"]


def test_nb_mark_output_code():
    """test mark_output code - if no source, marked as code"""
    # source marked as hide, code output
    nb = create_test_nb(code_source="# hide_input\n# output_code\nsome code")
    nb_process_hide_flags(nb)
    assert nb.cells[0].source == ""
    assert nb.cells[0].metadata.get("output_type", "") == "code"
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_CODE in outputs[0]["data"]["text/plain"]
    assert "<pre>" in outputs[0]["data"]["text/plain"]
    assert OUTPUT_CODE_CLOSE in outputs[1]["text"]
    assert "<pre>" in outputs[1]["text"]

    nb = create_test_nb(code_source="")
    nb.cells[0].metadata["output_type"] = "code"
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_CODE in outputs[0]["data"]["text/plain"]
    assert "<pre>" in outputs[0]["data"]["text/plain"]
    assert OUTPUT_CODE_CLOSE in outputs[1]["text"]
    assert "<pre>" in outputs[1]["text"]


def test_nb_mark_output_collapse():
    "test mark_output_collapse" ""
    nb = create_test_nb(code_source="#collapse_output\nsome code")
    nb_mark_output(nb)
    outputs = nb.cells[0].outputs
    assert OUTPUT_FLAG_COLLAPSE in outputs[0]["data"]["text/plain"]
    assert OUTPUT_FLAG_COLLAPSE not in outputs[1]["text"]
    assert "#collapse_output" not in nb.cells[0].source


def test_MarkOutputPreprocessor():
    """test MarkOutputPreprocessor"""
    processor = MarkOutputPreprocessor()
    processor.enabled = True
    nb = create_test_nb(code_source="some code")
    nb, _ = processor(nb, {})
    outputs = nb.cells[0].outputs
    assert OUTPUT_FLAG in outputs[0]["data"]["text/plain"]
    assert OUTPUT_FLAG not in outputs[1]["text"]


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
