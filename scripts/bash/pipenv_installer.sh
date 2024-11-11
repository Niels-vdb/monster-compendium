#!/bin/bash

# Checks if pipenv is in one of PATH, if not downloads pipenv
if ! command -v pipenv &> /dev/null; then
    echo "Pipenv is not installed, start installing"
    pip install pipenv
else
    echo "Pipenv already installed, continuing"
fi

echo "Installing all dependencies with pipenv"
pipenv run sh install
echo "All dependencies installed"