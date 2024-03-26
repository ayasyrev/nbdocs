
from nbdocs.convert import MdConverter
from nbdocs.tests.base import create_test_nb, create_test_outputs

converter = MdConverter()
nb = create_test_nb(code_source="some_code", code_outputs=create_test_outputs())
result_1 = """\
<!-- cell #0 code -->


```
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



![png](output_1_2.png)


"""


def test_base():
    """test base convert"""
    md, _ = converter.from_nb(nb)
    assert md == result_1
