from nbformat import v4 as nbformat

from nbdocs.convert import MdConverter
from nbdocs.tests.base import create_test_nb, create_test_outputs

converter = MdConverter()
nb = create_test_nb(code_source="some_code", code_outputs=create_test_outputs())
result_1 = """```
some_code
```
<details open> <summary>output</summary>
    <pre>
    - test/plain in output
    </pre>


    <pre>
    - text in stdout (stream) output
    </pre>
</details>



![png](output_0_2.png)


"""


def test_base():
    """test base convert"""
    md, _ = converter.nb2md(nb)
    assert md == result_1


def test_angle_brackets():
    """test angle brackets"""
    nb.cells[0].outputs[0].data["text/plain"] = "<class 'some_lib.SomeClass1'>"
    md, _ = converter.nb2md(nb)
    assert "<pre>\n    class 'some_lib.SomeClass1'\n    </pre>" in md
    assert "<class" not in md

    nb.cells[0].outputs[0].data["text/plain"] = "<class 'some_lib.SomeClass1'>\n"
    md, _ = converter.nb2md(nb)
    assert "<pre>\n    class 'some_lib.SomeClass1'\n    </pre>" in md
    assert "<class" not in md

    nb.cells[0].outputs[0].data["text/plain"] = ""
    nb.cells[0].outputs[1].text = "<class 'some_lib.SomeClass2'>"
    md, _ = converter.nb2md(nb)
    assert "<pre>\n    class 'some_lib.SomeClass2'\n    </pre>" in md
    assert "<class" not in md

    nb.cells[0].outputs[1].text = "<class 'some_lib.SomeClass2'>\n"
    md, _ = converter.nb2md(nb)
    assert "<pre>\n    class 'some_lib.SomeClass2'\n    </pre>" in md
    assert "<class" not in md


def test_process_output_text():
    """test process_output_text"""
    # remove Output()
    text = "Output()"
    assert process_output_text(text, "") == ""
    # remove empty <pre></pre>
    text = "<pre class=some_class></pre>"
    assert process_output_text(text, "") == ""
    # remove <pre>\n</pre>
    text = "<pre class=some_class>\n</pre>"
    assert process_output_text(text, "") == ""
    # add <pre> to simple text
    text = "text"
    assert process_output_text(text, "") == "<pre>\ntext\n</pre>"
    # do nothing if text with <pre></pre>
    text = "<pre>text</pre>"
    assert process_output_text(text, "") == "<pre>text</pre>"


def test_get_out_node():
    """test get_out_node"""
    output = nbformat.new_output("stream", name="stdout", text="(stream) output")
    node, name = get_out_node(output)
    assert name == "text"
    assert node == {
        "output_type": "stream",
        "name": "stdout",
        "text": "(stream) output",
    }
    output = nbformat.new_output(
        "display_data", data={"text/plain": "test/plain in output"}
    )
    node, name = get_out_node(output)
    assert name == "text/plain"
    assert node == {"text/plain": "test/plain in output"}
    output = nbformat.new_output("display_data", data={"image/png": "Zw=="})
    node, name = get_out_node(output)
    assert name is None
    assert node is None
    output = nbformat.new_output(
        "display_data", data={"text/html": "test/html in output"}
    )
    node, name = get_out_node(output)
    assert name == "text/html"
    assert node == {"text/html": "test/html in output"}
    # both "text/html" and "text/plain"
    output = nbformat.new_output(
        "display_data",
        data={
            "text/plain": "test/plain in output",
            "text/html": "test/html in output",
        },
    )
    node, name = get_out_node(output)
    assert name == "text/html"
    assert node == {
        "text/plain": "test/plain in output",
        "text/html": "test/html in output",
    }
