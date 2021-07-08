# zkeys

Display Zsh key bindings in more human-readable formats.

For example, print a table of key bindings, sorted by widget (i.e. function):

```text
% zkeys
...
^B        backward-char
^[[D      backward-char
^[OD      backward-char
^?        backward-delete-char
^H        backward-delete-char
^[^?      backward-kill-word
^[^H      backward-kill-word
^[B       backward-word
^[b       backward-word
^A        beginning-of-line
^[OH      beginning-of-line
^[C       capitalize-word
^[c       capitalize-word
^L        clear-screen
^[^L      clear-screen
...
```

Instead of:

```text
% bindkey
"^@" set-mark-command
"^A" beginning-of-line
"^B" backward-char
"^D" delete-char-or-list
"^E" end-of-line
"^F" forward-char
"^G" send-break
"^H" backward-delete-char
...
"^[B" backward-word
"^[C" capitalize-word
"^[D" kill-word
"^[F" forward-word
...
```

Run `zkeys -h` to see more sorting and grouping options.

By default, `zkeys` runs `bindkey -L` in a Zsh subprocess. It can also read from standard input, which is faster, and enables displaying the current shell configuration:

```sh
bindkey -L | zkeys
```

To learn about Zsh key bindings, see:

- <https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html>
- <https://zsh.sourceforge.io/Doc/Release/User-Contributions.html#Widgets>

## Installing

Requires Python 3.8 or newer.

Install the latest release from [PyPI](https://pypi.org/project/zkeys/) using [pipx](https://pypa.github.io/pipx/) (recommended) or [pip](https://pip.pypa.io/en/stable/):

```sh
pipx install zkeys

python3 -m pip install -U zkeys
```

To install the latest version from GitHub, replace `zkeys` with `git+https://github.com/bhrutledge/zkeys.git`.
