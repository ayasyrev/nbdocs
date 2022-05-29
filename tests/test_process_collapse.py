from nbdocs.process import (
    MarkOutputPreprocessor,
    format_output,
    md_process_collapse_output,
    md_process_output_flag,
    nb_mark_output,
    output_flag,
)

from nbdocs.tests.base import create_nb


def test_nb_mark_output():
    "test mark_output" ""
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


md_collapse = """
```python
#collapse_output
some code
```
???+ done "output"  
    <pre>Some output
      output sec line
        more output

```python
#collapse_output
more code
```
???+ done "output"  
    <pre>Some output
      output sec line
        more output

"""


def test_md_process_collapse_output():
    """test md_process_collapse_output"""
    md = md_process_collapse_output(md_collapse)
    assert "??? done" in md
    # assert "???+" not in md
