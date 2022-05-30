from configparser import ConfigParser
import configparser
from pathlib import Path, PosixPath
from typing import List, Optional, Union, TypeVar

# import toml

from pydantic import BaseModel


PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)


class Config(BaseModel):
    """Config schema with default settings.
    Use config file for overwrite."""
    notebooks_path: str = "nbs"
    docs_path: str = "docs"
    images_path: str = "images"


# possible setting file names, section names to put config. If both exists first will be used.
# NAMES = [".nbdocs", "pyproject.toml"]
NAMES = [".nbdocs"]
SECTION_NAME = "nbdocs"


def get_config_name(
    config_path: Union[PosixPath, Path, str, None] = None, config_names: Optional[List[str]] = None
) -> Union[PosixPath, Path, None]:
    """get cfg name"""
    cfg_path = Path(config_path or ".").absolute()
    config_names = config_names or NAMES
    # if at root - return None, no cfg
    if cfg_path == cfg_path.parent:
        return None

    for config_name in config_names:
        if (result := cfg_path / config_name).exists():
            return result

    return get_config_name(cfg_path.parent, config_names)


def get_config_ini(config_name: PathOrStr) -> Union[configparser.SectionProxy, None]:
    """return nbdocs config section from INI config."""
    cfg = ConfigParser()
    cfg.read(config_name)
    if cfg.has_section(SECTION_NAME):
        return cfg[SECTION_NAME]


# def get_config_toml(config_name: PosixPath):
#     """return nbdocs config section from TOML config."""
#     cfg_tool = toml.load(config_name).get("tool", None)
#     if cfg_tool is not None:
#         return cfg_tool.get(SECTION_NAME, None)


def get_config(
    config_path: Union[PathOrStr, None] = None, config_names: Optional[List[str]] = None
) -> Config:
    """Read nbdocs config.

    Args:
        config_path (PosixPath, optional): Path to start search config. Defaults to None.
        config_names (List[str], optional): List of possible filenames. Defaults to None.

    Returns:
        Config: Config.
    """
    cfg_name = get_config_name(config_path, config_names)
    if cfg_name is not None:
        return Config(**(get_config_ini(cfg_name) or {}))
    else:
        return Config()
