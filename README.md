voronoi
=======

[![](https://github.com/lycantropos/voronoi/workflows/CI/badge.svg)](https://github.com/lycantropos/voronoi/actions/workflows/ci.yml "Github Actions")
[![](https://codecov.io/gh/lycantropos/voronoi/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/voronoi "Codecov")
[![](https://img.shields.io/github/license/lycantropos/voronoi.svg)](https://github.com/lycantropos/voronoi/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/voronoi.svg)](https://badge.fury.io/py/voronoi "PyPI")

In what follows `python` is an alias for `python3.7` or `pypy3.7`
or any later version (`python3.8`, `pypy3.8` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions
```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository
```bash
python -m pip install --upgrade voronoi
```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/voronoi.git
cd voronoi
```

Install
```bash
python setup.py install
```

Usage
-----
```python
>>> from voronoi.diagram import Diagram
>>> diagram = Diagram()
>>> diagram.construct([], [])
>>> diagram.cells == diagram.edges == diagram.vertices == []
True
>>> from voronoi.point import Point
>>> diagram = Diagram()
>>> diagram.construct([Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)], [])
>>> from voronoi.faces import Vertex
>>> diagram.vertices == [Vertex(2, 2)]
True
>>> from voronoi.segment import Segment
>>> diagram.construct([], [Segment(Point(0, 0), Point(4, 0)),
...                        Segment(Point(4, 4), Point(0, 4))])
>>> diagram.vertices == [Vertex(2, 2), Vertex(0, 2), Vertex(4, 2)]
True

```
for `CPython` original C++ implementation can be invoked by importing from `_voronoi` module instead.

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies
```bash
python -m pip install --force-reinstall -r requirements-tests.txt
```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
