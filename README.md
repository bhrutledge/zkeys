# zkeys

Display Zsh key bindings in more human-readable formats.

Requires Python 3.8 or newer.

## Installation

Install the latest release from [PyPI](https://pypi.org/project/zkeys/) using [pipx](https://pypa.github.io/pipx/) (recommended) or [pip](https://pip.pypa.io/en/stable/):

```sh
pipx install zkeys

python3 -m pip install -U zkeys
```

Run `zkeys -h` to see usage.

## Developing

Create and activate a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments).

Make sure pip is up-to-date:

```sh
python3 -m pip install -U pip
```

Install this project in [development mode](https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#development-mode):

```sh
python3 -m pip install -e .
```

## Releasing

Activate the virtual environment.

Install the packages required for releasing:

```sh
python3 -m install -U build twine
```

Choose a version number and tag the release:

```sh
version=0.1.0

git tag -m "Release $version" $version
```

Create the [source distribution](https://packaging.python.org/glossary/#term-Source-Distribution-or-sdist) and [wheel](https://packaging.python.org/glossary/#term-Built-Distribution) packages:

```sh
python3 -c "import shutil; shutil.rmtree('dist', ignore_errors=True)"

python3 -m build

python3 -m twine check --strict dist/*
```

Publish the release to PyPI:

```sh
python3 -m twine upload dist/*
```

Push the release tag to GitHub:

```sh
git push origin $version
```
