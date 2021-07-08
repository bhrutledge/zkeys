import io
import re
import textwrap
from typing import List

import pytest
from pytest_console_scripts import ScriptRunner

SCRIPT_NAME = "zkeys"
SCRIPT_USAGE = f"usage: {SCRIPT_NAME} [-h] [--version]"


def test_prints_help(script_runner: ScriptRunner) -> None:
    result = script_runner.run(SCRIPT_NAME, "-h")
    assert result.success
    assert result.stdout.startswith(SCRIPT_USAGE)


def test_prints_help_for_invalid_option(script_runner: ScriptRunner) -> None:
    result = script_runner.run(SCRIPT_NAME, "-!")
    assert not result.success
    assert result.stderr.startswith(SCRIPT_USAGE)


def test_prints_version(script_runner: ScriptRunner) -> None:
    result = script_runner.run(SCRIPT_NAME, "--version")
    assert result.success
    assert re.match(rf"{SCRIPT_NAME} \d+\.\d", result.stdout)


def test_prints_keybindings_from_zsh(script_runner: ScriptRunner) -> None:
    result = script_runner.run(SCRIPT_NAME)
    assert result.success
    for line in result.stdout.splitlines():
        assert re.match(r"(?#string)[M^]\S+(?#space) +(?#widget)[-_a-z]+", line)


SCRIPT_INPUT = r"""
bindkey "^@" set-mark-command
bindkey "^L" clear-screen
bindkey "^Q" push-line
bindkey "^X^U" undo
bindkey "^X?" _complete_debug
bindkey "^Xu" undo
bindkey "^[^L" clear-screen
bindkey "^[\"" quote-region
bindkey "^['" quote-line
bindkey "^[Q" push-line
bindkey "^[[A" up-line-or-history
bindkey "^[[B" down-line-or-history
bindkey "^[q" push-line
bindkey "^_" undo
bindkey "\M-Q" push-line
bindkey "\M-q" push-line
"""


@pytest.mark.parametrize(
    "options,expected_output",
    [
        pytest.param(
            [],
            """
            ^X?       _complete_debug
            ^L        clear-screen
            ^[^L      clear-screen
            ^[[B      down-line-or-history
            ^Q        push-line
            ^[Q       push-line
            ^[q       push-line
            M-Q       push-line
            M-q       push-line
            ^['       quote-line
            ^["       quote-region
            ^@        set-mark-command
            ^_        undo
            ^Xu       undo
            ^X^U      undo
            ^[[A      up-line-or-history
            """,
            id="sorted_by_widget",
        ),
        pytest.param(
            ["-i"],
            """
            ^@        set-mark-command
            ^L        clear-screen
            ^Q        push-line
            ^_        undo
            ^["       quote-region
            ^['       quote-line
            ^[Q       push-line
            ^[q       push-line
            ^[^L      clear-screen
            M-Q       push-line
            M-q       push-line
            ^X?       _complete_debug
            ^Xu       undo
            ^X^U      undo
            ^[[A      up-line-or-history
            ^[[B      down-line-or-history
            """,
            id="sorted_by_string",
        ),
        pytest.param(
            ["-w"],
            """
            _complete_debug                         ^X?
            clear-screen                            ^L      ^[^L
            down-line-or-history                    ^[[B
            push-line                               ^Q      ^[Q     ^[q     M-Q     M-q
            quote-line                              ^['
            quote-region                            ^["
            set-mark-command                        ^@
            undo                                    ^_      ^Xu     ^X^U
            up-line-or-history                      ^[[A
            """,
            id="grouped_by_widget",
        ),
        pytest.param(
            ["-p"],
            """
            ^       @ L Q _
            ^[      " ' Q q
            ^[^     L
            M-      Q q
            ^X      ? u
            ^X^     U
            ^[[     A B
            """,
            id="grouped_by_prefix",
        ),
    ],
)
def test_prints_keybindings_from_stdin(
    options: List[str],
    expected_output: str,
    script_runner: ScriptRunner,
) -> None:
    stdin = io.StringIO(textwrap.dedent(SCRIPT_INPUT))

    result = script_runner.run(SCRIPT_NAME, *options, "-", stdin=stdin)
    assert result.success
    assert result.stdout.strip() == textwrap.dedent(expected_output).strip()
