
from nbdocs.convert import MdConverter

from nbdocs.tests.base import create_test_nb, create_test_outputs


converter = MdConverter()
nb = create_test_nb(code_source="some_code", code_outputs=create_test_outputs())
result_1 = """```
some_code
```
<details open> <summary>output</summary>  
    <pre>- test/plain in output</pre>


    <pre>- text in stdout (stream) output</pre>
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
    assert "<pre>class 'some_lib.SomeClass1'</pre>" in md
    assert "<class" not in md

    nb.cells[0].outputs[0].data["text/plain"] = "<class 'some_lib.SomeClass1'>\n"
    md, _ = converter.nb2md(nb)
    assert "<pre>class 'some_lib.SomeClass1'</pre>" in md
    assert "<class" not in md

    nb.cells[0].outputs[0].data["text/plain"] = ""
    nb.cells[0].outputs[1].text = "<class 'some_lib.SomeClass2'>"
    md, _ = converter.nb2md(nb)
    assert "<pre>class 'some_lib.SomeClass2'</pre>" in md
    assert "<class" not in md

    nb.cells[0].outputs[1].text = "<class 'some_lib.SomeClass2'>\n"
    md, _ = converter.nb2md(nb)
    assert "<pre>class 'some_lib.SomeClass2'</pre>" in md
    assert "<class" not in md
