from pathlib import Path
from nbdocs.core import get_nb_names, read_nb, write_nb

# get_nb_names("sdf")
nb_path = Path("tests/test_nbs")
nb_name = "nb_1.ipynb"
nb_filename = nb_path / nb_name
nb = read_nb(nb_filename)
print(nb.filename)

new_name = "tmp"
dest_name = nb_path / new_name
print (f"{dest_name=}")
write_nb(nb, nb_path / new_name)
print(f"{dest_name.with_suffix('.ipynb')}")

nb.pop("filename", None)
nb.pop("filename", None)