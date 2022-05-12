from pathlib import PosixPath
from typing import List

import pytest
from nbdocs.settings import NAMES, SECTION_NAMES, get_config, get_config_name


def create_config(config_path: PosixPath, config_name: str, section: str, arg_names: List[str]):
    """create config file"""
    with open(config_path / config_name, "w", encoding="utf-8") as fh:
        fh.write(f"[{section}]\n")
        for arg in arg_names:
            fh.write(f"{arg} = test_{arg}\n")


def test_get_config_name_no_config(tmp_path: PosixPath):
    """test get_config_name no config"""
    config_path = tmp_path
    config_name = get_config_name(config_path=config_path)
    assert config_name is None


test_args = ["notebook_path", "doc_path", "image_path"]


@pytest.mark.parametrize("config_name", NAMES)
@pytest.mark.parametrize("section_name", SECTION_NAMES)
def test_get_config_name(tmp_path: PosixPath, config_name, section_name):
    """test get_config_name"""
    config_path = tmp_path
    for arg in test_args:  # args one by one
        create_config(tmp_path, config_name, section_name, [arg])
        assert (tmp_path / config_name).exists()

        cfg_name = get_config_name(config_path=config_path)
        assert cfg_name.exists()
        cfg = get_config(cfg_name)
        assert cfg is not None
        test_arg = cfg.get(arg, None)
        assert test_arg == f"test_{arg}"

    # all args
    create_config(tmp_path, config_name, section_name, test_args)
    assert (tmp_path / config_name).exists()

    cfg_name = get_config_name(config_path=config_path)
    assert cfg_name.exists()
    cfg = get_config(cfg_name)
    assert cfg is not None
    for arg in test_args:
        test_arg = cfg.get(arg, None)
        assert test_arg == f"test_{arg}"
    # no args
    create_config(tmp_path, config_name, section_name, test_args)
    assert (tmp_path / config_name).exists()


def test_get_config_name_no_section(tmp_path: PosixPath):
    """test get_config_name cfg w/o section"""

    create_config(tmp_path, NAMES[0], "wrong_name", ["wrong_arg"])

    cfg_name = get_config_name(config_path=tmp_path)
    assert cfg_name.exists()

    cfg = get_config(cfg_name)
    assert cfg is None
