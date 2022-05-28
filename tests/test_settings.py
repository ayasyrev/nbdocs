import configparser
from pathlib import PosixPath
from typing import List

from nbdocs.settings import (
    NAMES,
    get_config,
    get_config_ini,
    get_config_name,
    get_config_toml,
    Config
    # merge_cfg,
    # nbdocs_def_cfg,
)


def create_config(
    config_path: PosixPath, config_name: str, section: str, arg_names: List[str]
):
    """create config file"""
    with open(config_path / config_name, "w", encoding="utf-8") as fh:
        fh.write(f"[{section}]\n")
        for arg in arg_names:
            fh.write(f"{arg} = test_{arg}\n")


def test_get_config_name_no_config(tmp_path: PosixPath):
    """test get_config_name no config"""
    config_name = get_config_name(config_path=tmp_path)
    assert config_name is None


def test_get_config_name_def():
    """test get_config_name default"""
    # default - load TOML from app root
    config_name = get_config_name()
    assert config_name.name == NAMES[0]
    cfg = get_config_toml(config_name)
    assert cfg is not None
    assert isinstance(cfg, dict)


def test_get_config_name_ini():
    """test get_config_name default"""
    # default - load TOML from app root
    config_name = get_config_name("tests/")
    assert config_name.name == NAMES[1]
    cfg = get_config_ini(config_name)
    assert cfg is not None
    assert isinstance(cfg, configparser.SectionProxy)


def test_get_config(tmp_path):
    """ test get_config"""
    # def - toml from root
    cfg = get_config()
    assert isinstance(cfg, Config)
    assert cfg.notebooks_path == "nbs"
    # ini from tests
    cfg = get_config("tests")
    assert isinstance(cfg, Config)
    assert cfg.notebooks_path == "nbs"
    # empty ini
    cfg_name = NAMES[1]
    create_config(tmp_path, cfg_name, "wrong_section", [])
    cfg = get_config(tmp_path)
    assert isinstance(cfg, Config)
    def_cfg = Config()
    assert def_cfg == cfg

    create_config(tmp_path, cfg_name, "nbdocs", ["docs_path"])
    cfg = get_config(tmp_path)
    # assert cfg is not None
    assert cfg.docs_path == "test_docs_path"
