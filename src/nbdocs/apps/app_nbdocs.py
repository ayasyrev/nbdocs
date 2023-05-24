import sys
from dataclasses import dataclass
from typing import Optional, Sequence

from argparsecfg import ArgumentParserCfg, field_argument, create_parser, create_dc_obj, add_args_from_dc
from rich import print as rprint

from nbdocs.convert import convert2md, filter_changed
from nbdocs.core import get_nb_names
from nbdocs.settings import get_config

parser_cfg = ArgumentParserCfg(description="NbDocs. Convert notebooks to docs. Default to .md")


@dataclass
class AppConfig:
    force: bool = field_argument(
        "-F",
        default=False,
        help="Force convert all notebooks.",
    )


def nbdocs(app_cfg: AppConfig,) -> None:
    """NbDocs. Convert notebooks to docs. Default to .md"""
    cfg = get_config()
    nb_names = get_nb_names(cfg.notebooks_path)
    nbs_number = len(nb_names)
    if nbs_number == 0:
        rprint("No files to convert!")
        sys.exit()
    rprint(f"Found {nbs_number} notebooks.")
    if not app_cfg.force:
        message = "Filtering notebooks with changes... "
        nb_names = filter_changed(nb_names, cfg)
        if len(nb_names) == nbs_number:
            message += "No changes."
        rprint(message)

    if len(nb_names) == 0:
        rprint("No files to convert!")
        sys.exit()

    rprint(f"To convert: {len(nb_names)} notebooks.")
    convert2md(nb_names, cfg)


def main(args: Optional[Sequence[str]] = None) -> None:
    parser = create_parser(parser_cfg)
    add_args_from_dc(parser, AppConfig)
    parsed_args = parser.parse_args(args=args)
    app_cfg = create_dc_obj(AppConfig, parsed_args)
    nbdocs(app_cfg)


if __name__ == "__main__":
    main()
