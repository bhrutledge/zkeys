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

    @property
    def prefix(self) -> str:
        return self.in_string[:-1]

    @property
    def character(self) -> str:
        return self.in_string[-1]

    def prefix_comparison(self) -> Tuple[int, str]:
        prefix_rank = self.PREFIXES.get(self.prefix, 999)
        return (prefix_rank, self.character.upper())

    def widget_comparison(self) -> Tuple[str, int, str]:
        return (self.widget, *self.prefix_comparison())


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

    input_lines = (line.strip() for line in args.file) if args.file else run_bindkey()
    bindings = list(parse_bindkey(input_lines))

    if args.widget:
        output_lines = group_by_widget(bindings)
    elif args.prefix:
        output_lines = group_by_prefix(bindings)
    elif args.in_string:
        output_lines = sort_by_in_string(bindings)
    else:
        output_lines = sort_by_widget(bindings)

    for line in output_lines:
        print(line)


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
        if widget in Keybinding.IGNORE_WIDGETS:
            continue

        # HACK: Remove slashes for readability, e.g. \M-\$ becomes M-$
        # Could be overzealous, esp. with custom keybindings
        in_string = in_string.replace("\\", "")
        yield Keybinding(in_string, widget)


def group_by_widget(bindings: Iterable[Keybinding]) -> Iterable[str]:
    widgets = group_bindings(
        sorted(bindings, key=Keybinding.widget_comparison),
        key_attr="widget",
        value_attr="in_string",
    )

    widget_width = max(len(b.widget) for b in bindings) + 4
    in_string_width = max(len(b.in_string) for b in bindings) + 4

    for widget, in_strings in widgets.items():
        in_strings = [f"{s:{in_string_width}}" for s in in_strings]
        yield f"{widget:{widget_width}}{' '.join(in_strings).strip()}"


def group_by_prefix(bindings: Iterable[Keybinding]) -> Iterable[str]:
    prefixes = group_bindings(
        sorted(bindings, key=Keybinding.prefix_comparison),
        key_attr="prefix",
        value_attr="character",
    )

    prefix_width = max(len(b.prefix) for b in bindings) + 4

    for prefix, characters in prefixes.items():
        yield f"{prefix:{prefix_width}}{' '.join(characters).strip()}"


def sort_by_in_string(bindings: Iterable[Keybinding]) -> Iterable[str]:
    in_string_width = max(len(b.in_string) for b in bindings) + 4

    for binding in sorted(bindings, key=Keybinding.prefix_comparison):
        yield f"{binding.in_string:{in_string_width}}{binding.widget}"


def sort_by_widget(bindings: Iterable[Keybinding]) -> Iterable[str]:
    in_string_width = max(len(b.in_string) for b in bindings) + 4

    for binding in sorted(bindings, key=Keybinding.widget_comparison):
        yield f"{binding.in_string:{in_string_width}}{binding.widget}"


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
