"""Display Zsh key bindings in more human-readable formats."""
import argparse
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from importlib import metadata
from typing import Dict, Iterable, List, Tuple

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


Row = Tuple[str, List[str]]


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
        rows = group_by_widget(bindings)
    elif args.prefix:
        rows = group_by_prefix(bindings)
    elif args.in_string:
        rows = sort_by_in_string(bindings)
    else:
        rows = sort_by_widget(bindings)

    for output_line in format_table(rows):
        print(output_line)


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


def group_by_widget(bindings: Iterable[Keybinding]) -> Iterable[Row]:
    widgets: Dict[str, List[str]] = defaultdict(list)

    for binding in sorted(bindings, key=Keybinding.widget_comparison):
        widgets[binding.widget].append(binding.in_string)

    return widgets.items()


def group_by_prefix(bindings: Iterable[Keybinding]) -> Iterable[Row]:
    prefixes: Dict[str, List[str]] = defaultdict(list)

    for binding in sorted(bindings, key=Keybinding.prefix_comparison):
        prefixes[binding.prefix].append(binding.character)

    return prefixes.items()


def sort_by_in_string(bindings: Iterable[Keybinding]) -> List[Row]:
    return [
        (binding.in_string, [binding.widget])
        for binding in sorted(bindings, key=Keybinding.prefix_comparison)
    ]


def sort_by_widget(bindings: Iterable[Keybinding]) -> List[Row]:
    return [
        (binding.in_string, [binding.widget])
        for binding in sorted(bindings, key=Keybinding.widget_comparison)
    ]


def format_table(rows: Iterable[Row]) -> Iterable[str]:
    key_width = max(len(k) for k, _ in rows) + 4
    value_width = max(len(v) for _, values in rows for v in values)

    for key, values in rows:
        values = [f"{v:{value_width}}" for v in values]
        yield f"{key:{key_width}}{' '.join(values).strip()}"


if __name__ == "__main__":  # pragma: no cover
    main()
