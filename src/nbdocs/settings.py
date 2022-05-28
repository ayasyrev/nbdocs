from configparser import ConfigParser
from pathlib import Path, PosixPath
from typing import List, Union

import toml

# Defaults: if no config file, use this
nbdocs_def_cfg = dict(
    notebooks_path="nbs",
    docs_path="docs",
    images_path="images")

# possible setting file names, section names to put config
NAMES = ["pyproject.toml", ".nbdocs"]
SECTION_NAME = "nbdocs"


def get_config_name(
    config_path: Union[PosixPath, str, None] = None, config_names: List[str] = None
) -> PosixPath:
    """get cfg"""
    cfg_path = Path(config_path or ".").absolute()
    config_names = config_names or NAMES
    # if at root - return None, no cfg
    if cfg_path == cfg_path.parent:
        return None

    for config_name in config_names:
        if (result := cfg_path / config_name).exists():
            return result

    return get_config_name(cfg_path.parent, config_names)


def get_config_ini(config_name: PosixPath):
    """return nbdocs config section from INI config."""
    cfg = ConfigParser()
    cfg.read(config_name)
    if cfg.has_section(SECTION_NAME):
        return cfg[SECTION_NAME]
    else:
        return None


def get_config_toml(config_name: PosixPath):
    """return nbdocs config section from TOML config."""
    cfg = toml.load(config_name)
    return cfg["tool"][SECTION_NAME]


def get_config(
    config_path: Union[PosixPath, str, None] = None, config_names: List[str] = None
) -> Union[dict, None]:
    """Read nbdocs config.

    Args:
        config_path (PosixPath, optional): Path to start search config. Defaults to None.
        config_names (List[str], optional): List of possible filenames. Defaults to None.

    Returns:
        Union[dict, None]: Dict config.
    """
    if (cfg_name := get_config_name(config_path, config_names)):
        if cfg_name.name == NAMES[0]:  # "pyproject.toml"
            return get_config_toml(cfg_name)
        else:
            return get_config_ini(cfg_name)


def merge_cfg(cfg: dict, def_cfg: dict = None) -> dict:
    """Merge config with default one."""
    merged_cfg = {}
    def_cfg = def_cfg or nbdocs_def_cfg
    for key, value in def_cfg.items():
        merged_cfg[key] = cfg.get(key, None) or value
    return merged_cfg


def read_config(
    config_path: Union[PosixPath, str, None] = None, config_names: List[str] = None
) -> Union[dict, None]:
    cfg = get_config(config_path, config_names)
    return merge_cfg(cfg)
