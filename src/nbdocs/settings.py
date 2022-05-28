from configparser import ConfigParser
from pathlib import Path, PosixPath
from typing import List, Union

import toml

from pydantic import BaseModel


# Defaults: if no config file, use this
class Config(BaseModel):
    notebooks_path: str = "nbs",
    docs_path: str = "docs",
    images_path: str = "images"


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
    cfg_tool = toml.load(config_name).get("tool", None)
    if cfg_tool is not None:
        return cfg_tool.get(SECTION_NAME, None)


def get_config(
    config_path: Union[PosixPath, str, None] = None, config_names: List[str] = None
) -> Config:
    """Read nbdocs config.

    Args:
        config_path (PosixPath, optional): Path to start search config. Defaults to None.
        config_names (List[str], optional): List of possible filenames. Defaults to None.

    Returns:
        Config: Config.
    """
    if (cfg_name := get_config_name(config_path, config_names)):
        if cfg_name.name == NAMES[0]:  # "pyproject.toml"
            return Config(**(get_config_toml(cfg_name) or {}))
        else:
            return Config(**(get_config_ini(cfg_name) or {}))
