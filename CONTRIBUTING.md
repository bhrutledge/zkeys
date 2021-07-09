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

Create a [PyPI API token](https://pypi.org/manage/account/#api-tokens) for this project, and add it to a [GitHub Actions repository secret](https://github.com/bhrutledge/zkeys/settings/secrets/actions) named `PYPI_TOKEN`.

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

Watch the release on [GitHub Actions](https://github.com/bhrutledge/zkeys/actions/workflows/main.yml).

View the release on [PyPI](https://pypi.org/project/zkeys/).
