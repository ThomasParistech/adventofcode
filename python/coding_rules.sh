#!/bin/bash

ruff check --config .vscode/ruff.toml --fix --select F401 .
isort --py 310 --force-single-line-imports --line-length 120 --dont-order-by-type --multi-line 3 --use-parentheses --tc .
mypy . --config-file .vscode/.mypy.ini

