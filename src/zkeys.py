"""Display Zsh key bindings in more human-readable formats."""
import argparse
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from importlib import metadata
from typing import Dict, Iterable, List, Literal, Tuple

try:
    __version__ = metadata.version("zkeys")
except metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType("r"),
        help="read lines from file ('-' for stdin)",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--in-string",
        action="store_true",
        help="sort by in-string instead of widget",
    )
    group.add_argument(
        "-w",
        "--widget",
        action="store_true",
        help="group by widget",
    )
    group.add_argument(
        "-p",
        "--prefix",
        action="store_true",
        help="group by prefix",
    )
    args = parser.parse_args()

    lines = (line.strip() for line in args.file) if args.file else run_bindkey()
    bindings = parse_bindkey(lines)

    if args.widget:
        widgets = group_bindings(
            sorted(bindings, key=lambda b: (b.widget, b.rank)),
            key_attr="widget",
            value_attr="in_string",
        )
        for widget, in_strings in widgets.items():
            in_strings = [f"{in_string:7}" for in_string in in_strings]
            print(f"{widget:40}{' '.join(in_strings)}".strip())

    elif args.prefix:
        prefixes = group_bindings(
            sorted(bindings),
            key_attr="prefix",
            value_attr="character",
        )
        for prefix, characters in prefixes.items():
            print(f"{prefix:8}{' '.join(characters)}".strip())

    elif args.in_string:
        for binding in sorted(bindings):
            print(f"{binding.in_string:10}{binding.widget}")

    else:
        for binding in sorted(bindings, key=lambda b: (b.widget, b.rank)):
            print(f"{binding.in_string:10}{binding.widget}")


PREFIXES = {
    prefix: rank
    for rank, prefix in enumerate(
        [
            "^",
            "^[",
            "^[^",
            "M-",
            "M-^",
            "^X",
            "^X^",
            "^[[",
            "^[O",
            "^[[3",
        ]
    )
}


IGNORE_WIDGETS = {
    "bracketed-paste",
    "digit-argument",
    "neg-argument",
    "self-insert-unmeta",
}


@dataclass
class Keybinding:
    """
    Map an in-string like '^[b' to a ZLE widget like 'backward-word'.

    >>> binding = Keybinding('^[b', 'backward-word')
    >>> binding.in_string
    '^[b'
    >>> binding.prefix
    '^['
    >>> binding.character
    'b'
    >>> binding.widget
    'backward-word'
    """

    in_string: str
    widget: str

    @property
    def prefix(self) -> str:
        return self.in_string[:-1]

    @property
    def character(self) -> str:
        return self.in_string[-1]

    @property
    def rank(self) -> Tuple[int, str]:
        prefix_rank = PREFIXES.get(self.prefix, 999)
        return (prefix_rank, self.character.upper())

    def __lt__(self, other: "Keybinding") -> bool:
        return self.rank < other.rank


def run_bindkey() -> Iterable[str]:
    result = subprocess.run(
        ["zsh", "--login", "--interactive", "-c", "bindkey -L"],
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def parse_bindkey(lines: Iterable[str]) -> Iterable[Keybinding]:
    """Parse lines like 'bindkey "^[b" backward-word' into Keybinding objects."""
    pattern = r'bindkey "(?P<in_string>.+)" (?P<widget>.+)'

    for line in lines:
        if not (match := re.match(pattern, line)):
            continue

        in_string, widget = match.groups()
        if widget in IGNORE_WIDGETS:
            continue

        # HACK: Remove slashes for readability, e.g. \M-\$ becomes M-$
        # Could be overzealous, esp. with custom keybindings
        in_string = in_string.replace("\\", "")
        yield Keybinding(in_string, widget)


def group_bindings(
    bindings: Iterable[Keybinding],
    *,
    key_attr: Literal["widget", "prefix"],
    value_attr: Literal["in_string", "character"],
) -> Dict[str, List[str]]:
    """"""
    group: Dict[str, List[str]] = defaultdict(list)

    for binding in bindings:
        group[getattr(binding, key_attr)].append(getattr(binding, value_attr))

    return group


if __name__ == "__main__":  # pragma: no cover
    main()
