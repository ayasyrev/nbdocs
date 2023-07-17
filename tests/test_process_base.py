
from nbdocs.convert import MdConverter

from nbdocs.tests.base import create_test_nb, create_test_outputs


converter = MdConverter()
nb = create_test_nb(code_source="some_code", code_outputs=create_test_outputs())
result_1 = """```
some_code
```
<details open> <summary>output</summary>  
    <pre>- test/plain in output</pre>
</details>
<details open> <summary>output</summary>  
    <pre>- text in stdout (stream) output</pre>
</details>


    
![png](output_0_2.png)
    

"""


def test_base():
    """test base convert"""
    md, _ = converter.nb2md(nb)
    assert md == result_1
