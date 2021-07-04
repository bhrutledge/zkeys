import io
import re
import textwrap

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


def test_sorts_keybindings_by_widget(script_runner: ScriptRunner) -> None:
    script_input = textwrap.dedent(
        r"""
        bindkey "^@" set-mark-command
        bindkey "^L" clear-screen
        bindkey "^Q" push-line
        bindkey "^X^U" undo
        bindkey "^X?" _complete_debug
        bindkey "^Xu" undo
        bindkey "^[^L" clear-screen
        bindkey "^[!" expand-history
        bindkey "^[\"" quote-region
        bindkey "^['" quote-line
        bindkey "^[Q" push-line
        bindkey "^[[A" up-line-or-history
        bindkey "^[[B" down-line-or-history
        bindkey "^[q" push-line
        bindkey "^[^?" backward-kill-word
        bindkey "^_" undo
        bindkey "\M-Q" push-line
        bindkey "\M-q" push-line
        """
    )

    expected_output = textwrap.dedent(
        """
        ^X?       _complete_debug
        ^[^?      backward-kill-word
        ^L        clear-screen
        ^[^L      clear-screen
        ^[[B      down-line-or-history
        ^[!       expand-history
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
        """
    )

    result = script_runner.run(SCRIPT_NAME, "-", stdin=io.StringIO(script_input))
    assert result.success
    assert result.stdout.strip() == expected_output.strip()
