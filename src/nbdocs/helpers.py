from typing import Optional, Sequence


# print termynal output.
# termynal - animated terminal window. https://github.com/daxartio/termynal
# based on https://github.com/ines/termynal - termynal.js
def termynal_output(
    starter: str = "python",
    prog: str = "my_app.py",
    args: Optional[Sequence[str]] = None,
    out_text: str = "",
) -> None:
    """print termynal output"""
    if isinstance(args, Sequence):
        args_str = " ".join(args)
    else:
        args_str = args
    lines = [
        "<!-- termynal -->",
        "```",
        f"$ {starter} {prog} {args_str}",
        out_text,
        "\n```",
    ]
    print("\n".join(lines))
