"""
Display Zsh key bindings in more human-readable formats.

By default, this runs `bindkey -L` in a Zsh subprocess, and displays key bindings sorted
by widget (i.e. function). It can also read from standard input, which is faster, and
enables displaying the current shell configuration:

    bindkey -L | python3 zkeys.py -

To learn about Zsh key bindings, see:
https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#Zle-Widgets
https://zsh.sourceforge.io/Doc/Release/User-Contributions.html#Widgets
"""
import argparse
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from importlib import metadata
from typing import Dict, Iterable, List, Tuple

try:
    __version__ = metadata.version("zkeys")
except metadata.PackageNotFoundError:
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
        "-s",
        "--string",
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

    # TODO: Show human-readable keys, e.g. Esc instead of ^[
    # TODO: Indicate non-printing characters (e.g. space)
    # TODO: Use a PyPI package for table output

    lines = (line.strip() for line in args.file) if args.file else run_bindkey()
    bindings = sorted(parse_bindkey(lines))

    if args.widget:
        widgets = group_bindings(bindings)

        for widget, bindings in sorted(widgets.items()):
            strings = (b.string for b in bindings)
            print(f"{widget:40}{''.join(f'{s:8}' for s in strings)}")

    elif args.prefix:
        prefixes = group_bindings(bindings, key="prefix")

        for prefix, bindings in prefixes.items():
            keys = (b.key for b in bindings)
            print(f"{prefix:8}{' '.join(keys)}")

    else:
        if not args.string:
            bindings = sorted(bindings, key=lambda b: b.widget)

        for binding in bindings:
            print(f"{binding.string:10}{binding.widget}")


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
    string: str
    widget: str

    @property
    def prefix(self) -> str:
        return self.string[:-1]

    @property
    def key(self) -> str:
        return self.string[-1]

    @property
    def _compare_string(self) -> Tuple[int, str]:
        return (PREFIXES.get(self.prefix, 999), self.key.upper())

    def __lt__(self, other: "Keybinding") -> bool:
        return self._compare_string < other._compare_string


def run_bindkey() -> Iterable[str]:
    result = subprocess.run(
        ["zsh", "--login", "--interactive", "-c", "bindkey -L"],
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def parse_bindkey(lines: Iterable[str]) -> Iterable[Keybinding]:
    # bindkey "^A" beginning-of-line
    # TODO: Parse other types of bindings, e.g. -s
    pattern = r'bindkey "(?P<string>.+)" (?P<widget>.+)'

    for line in lines:
        if not (match := re.match(pattern, line)):
            continue

        string, widget = match.groups()
        if widget in IGNORE_WIDGETS:
            continue

        # HACK: Remove slashes for readability, e.g. \M-\$ becomes M-$
        # Could be overzealous, esp. with custom keybindings
        string = string.replace("\\", "")
        yield Keybinding(string, widget)


def group_bindings(
    bindings: Iterable[Keybinding],
    *,
    key: str = "widget",
) -> Dict[str, List[Keybinding]]:

    group: Dict[str, List[Keybinding]] = defaultdict(list)
    for binding in bindings:
        group[getattr(binding, key)].append(binding)

    return group


if __name__ == "__main__":
    main()
