# type: ignore
import re

SCRIPT_NAME = "zkeys"
SCRIPT_USAGE = f"usage: {SCRIPT_NAME} [-h] [--version]"


def test_prints_help(script_runner):
    result = script_runner.run(SCRIPT_NAME, "-h")
    assert result.success
    assert result.stdout.startswith(SCRIPT_USAGE)


def test_prints_help_for_invalid_option(script_runner):
    result = script_runner.run(SCRIPT_NAME, "-!")
    assert not result.success
    assert result.stderr.startswith(SCRIPT_USAGE)


def test_prints_version(script_runner):
    result = script_runner.run(SCRIPT_NAME, "--version")
    assert result.success
    assert re.match(rf"{SCRIPT_NAME} \d+\.\d", result.stdout)


def test_prints_keybindings_from_zsh(script_runner):
    result = script_runner.run(SCRIPT_NAME)
    assert result.success
    for line in result.stdout.splitlines():
        assert re.match(r"(?#string)[M^]\S+(?#space) +(?#widget)[-_a-z]+", line)
