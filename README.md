# warpsearch

<p align="left">
  <img src="logo.png" width="300">
</p>


[![PyPI](https://img.shields.io/pypi/v/warpsearch.svg)](https://pypi.org/project/warpsearch/)
[![Changelog](https://img.shields.io/github/v/release/adtygan/warpsearch?include_prereleases&label=changelog)](https://github.com/adtygan/warpsearch/releases)
[![Tests](https://github.com/adtygan/warpsearch/actions/workflows/test.yml/badge.svg)](https://github.com/adtygan/warpsearch/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/adtygan/warpsearch/blob/master/LICENSE)

Your smol and local image search engine

## Installation

Install this tool using `pip`:
```bash
pip install warpsearch
```
## Usage

For help, run:
```bash
warpsearch --help
```
You can also use:
```bash
python -m warpsearch --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd warpsearch
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
