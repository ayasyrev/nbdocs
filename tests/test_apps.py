from pathlib import Path
from typer.testing import CliRunner

from nbdocs.apps.app_nbclean import app as app_nbclean

from nbdocs.apps.app_nb2md import app as app_nb2md


runner = CliRunner()


def test_app_nbclean_def():
    """Test default run"""
    result = runner.invoke(app_nbclean)
    assert result.exit_code == 0
    assert "Clean: nbs" in result.stdout


def test_app_nbclean_no_nb():
    """Test if no Nb at path aor path not exist"""
    result = runner.invoke(app_nbclean, ["."])
    assert result.exit_code == 1
    assert "No files to clean!" in result.stdout

    result = runner.invoke(app_nbclean, ["not_exist_path"])
    assert result.exit_code == 1
    assert "not exists!" in result.stdout


def test_app_nbclean():
    """Test nb folder and file run"""
    result = runner.invoke(app_nbclean, ["tests/test_nbs"])
    assert result.exit_code == 0
    assert "tests/test_nbs" in result.stdout

    result = runner.invoke(app_nbclean, ["tests/test_nbs/code_hide_cells.ipynb"])
    assert result.exit_code == 0
    assert "tests/test_nbs/code_hide_cells.ipynb" in result.stdout


def test_app_nb2md(tmp_path: Path):
    """test nb2md"""
    # run for one nb
    result = runner.invoke(
        app_nb2md, ["tests/test_nbs/nb_1.ipynb", "--dest", f"{str(tmp_path)}"]
    )
    # assert result.exit_code == 0
    # run for folder w/o nbs, no nb to process.
    result = runner.invoke(app_nb2md, ["tests/", "--dest", f"{tmp_path}"])
    assert result.exit_code == 0
    assert "No files to convert!" in result.stdout
    # run for folder with test nbs.
    result = runner.invoke(app_nb2md, ["tests/test_nbs/", "--dest", f"{tmp_path}"])
    assert result.exit_code == 0
    # check for result
    # run again - no changes in nbs
    result = runner.invoke(app_nb2md, ["tests/test_nbs/", "--dest", f"{tmp_path}"])
    assert result.exit_code == 0
    assert "No files with changes to convert!" in result.stdout
