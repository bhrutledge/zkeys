# Contributing

Suggestions, questions, and bug reports are welcome on the [issue tracker](https://github.com/bhrutledge/zkeys/issues). However, since this is a small personal project, I'm not expecting contributions. This guide is intended to be a reference for myself, and an example for others to use in their projects.

## Developing

Install [tox](https://tox.readthedocs.io/).

Run the linters, type checks, tests, and coverage:

```sh
# On all supported Python versions
tox

# In the current Python environment
tox -e py,coverage
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

To publish to [TestPyPI](https://packaging.python.org/guides/using-testpypi/) instead:

```sh
TWINE_REPOSITORY=testpypi tox -e release
```
