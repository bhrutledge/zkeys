# zkeys

Display Zsh key bindings in more human-readable formats.

Requires Python 3.8 or newer.

## Installation

Install the latest release from [PyPI](https://pypi.org/project/zkeys/) using [pipx](https://pypa.github.io/pipx/) (recommended) or [pip](https://pip.pypa.io/en/stable/):

```sh
pipx install zkeys

python3 -m pip install -U zkeys
```

To install the latest version from GitHub, replace `zkeys` with `git+https://github.com/bhrutledge/zkeys.git`.

Run `zkeys -h` to see usage.

## Developing

Install [tox](https://tox.readthedocs.io/).

Run the linters, type checks, tests, and coverage on all supported Python versions, or a specific version:

```sh
tox

tox -e py38,coverage
```

Auto-format the code:

```sh
tox -e format
```

Create and activate a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) for [development](https://tox.readthedocs.io/en/latest/example/devenv.html):

```sh
tox --devenv venv

source venv/bin/activate
```

Run the tests:

```sh
pytest
```

## Releasing

Choose a version number and tag the release:

```sh
version=0.1.0

git tag -m "Release $version" $version
```

Create the [source distribution](https://packaging.python.org/glossary/#term-Source-Distribution-or-sdist) and [wheel](https://packaging.python.org/glossary/#term-Built-Distribution) packages, then publish the release to PyPI:

```sh
tox -e release
```

Push the release tag to GitHub:

```sh
git push origin $version
```
