from configparser import ConfigParser
from pathlib import Path, PosixPath
from typing import List

# Defaults: if no config file, use this
NOTEBOOKS_PATH = "nbs"
DOCS_PATH = "docs"
IMAGES_PATH = "images"

# possible setting file names, section names to put config
NAMES = ["pyproject.toml", ".nbdocs"]
SECTION_NAMES = ["tool.nbdocs", "nbdocs"]


def get_config_name(
    config_path: PosixPath = None, config_names: List[str] = None
) -> PosixPath:
    """get cfg"""
    cfg_path = config_path or Path.cwd()
    config_names = config_names or NAMES
    # if at root - return None, no cfg
    if cfg_path == cfg_path.parent:
        return None

    for config_name in config_names:
        if (result := cfg_path / config_name).exists():
            return result

    return get_config_name(cfg_path.parent, config_names)


def get_config(config_name: PosixPath):
    """return nbdocs config section from config."""
    cfg = ConfigParser()
    cfg.read(config_name)
    section = None
    for section_name in SECTION_NAMES:
        if cfg.has_section(section_name):
            section = section_name
    return cfg[section] if section is not None else None


if (cfg_name := get_config_name()):
    nbdocs_cfg = get_config(config_name=cfg_name)


NOTEBOOKS_PATH = nbdocs_cfg.get("notebook_path", None) or NOTEBOOKS_PATH
DOCS_PATH = nbdocs_cfg.get("doc_path", None) or DOCS_PATH
IMAGES_PATH = nbdocs_cfg.get("image_path", None) or IMAGES_PATH
