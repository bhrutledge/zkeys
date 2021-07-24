# Contributing

Suggestions, questions, and bug reports are welcome on the [issue tracker](https://github.com/bhrutledge/zkeys/issues). However, since this is a small personal project, I'm not expecting contributions. This guide is intended to be a reference for myself, and an example for others to use in their projects.

## Developing

Install [tox](https://tox.readthedocs.io/).

Run the linters, type checks, tests, and coverage on all supported Python versions:

```sh
tox
```

- This requires having multiple versions of Python installed on your system; [pyenv](https://github.com/pyenv/pyenv) is a good tool for that
- This will run:
    - [isort](https://pycqa.github.io/isort/) and [black](https://black.readthedocs.io/en/stable/) to format the code
    - [flake8](http://flake8.pycqa.org/en/latest/) to check code and docstring style
    - [mypy](https://mypy.readthedocs.io/en/latest/) to check types
    - [pytest](https://docs.pytest.org/en/latest/) and [coverage.py](https://coverage.readthedocs.io/en/latest/) to run the tests
-  See the [tox configuration](tox.ini) for details

Run the linters, type checks, tests, and coverage in the current Python environment:

```sh
tox -e py,coverage
```

- Consider using [`pyenv local`](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local) to set the desired Python version

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

### Continuous integration

Every push and pull request is tested on all supported plaforms via [GitHub Actions](https://github.com/bhrutledge/zkeys/actions/workflows/main.yml).

## Releasing

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [PEP 440](https://www.python.org/dev/peps/pep-0440/), and uses [setuptools_scm](https://pypi.org/project/setuptools-scm/) to determine the version from the latest `git` tag.

Choose a version number:

```sh
version=0.2.0
```

Update the [changelog](./CHANGELOG.md):

```sh
git commit -a -m "Update changelog for $version"
```

Tag the release:

```sh
git tag -m "Release $version" $version

git push origin main $version
```

Wait for the [GitHub Actions workflow](https://github.com/bhrutledge/zkeys/actions/workflows/main.yml) to succeed.

Create the [source distribution](https://packaging.python.org/glossary/#term-Source-Distribution-or-sdist) and [wheel](https://packaging.python.org/glossary/#term-Built-Distribution) packages, then publish the release to [PyPI](https://pypi.org/project/zkeys/):

```sh
tox -e release
```

- To publish to [TestPyPI](https://packaging.python.org/guides/using-testpypi/) instead:

  ```sh
  TWINE_REPOSITORY=testpypi tox -e release
  ```

Create a [GitHub Release](https://github.com/bhrutledge/zkeys/releases) with a link to the [release on PyPI](https://pypi.org/project/zkeys/#history), and the heading in the [changelog](CHANGELOG.md).

