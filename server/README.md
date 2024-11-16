# Creature Compendium

<!-- Badges -->

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting started](#getting-started)
    - [Production](#production)
    - [Development](#development)
        - [Server](#server)
- [Usage](#usage)
- [Contributing](#contributing)
- [Testing](#testing)
- [Changelog](#changelog)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

## Features

## Getting started

> [!NOTE]
> This program runs on Python version 3.13

### Production

Not yet in production

### Development

#### Server

For a quick start using the server in full capacity you can run the following automated script
`./scripts/bash/project_setup.sh`.
This will:

- Install pipenv (if not yet on machine) and install all dependencies needed for the application.
- Copy the .env.example file to a .env file.
- Create a secret key in the .env file (Windows users have to copy the key from the stdout where it is printed).

##### Manual steps

If the automated script is not working to your liking please follow the manual steps below.

1. Copy the `.env.example` file and name it `.env`
2. Create a random string in your terminal or git bash

```shell
openssl rand -hex 32 
```

3. Paste the string into the .env file and fill out the other variables.
4. Install pipenv `pip install --user pipenv`
5. Create pipenv shell

```shell
pipenv shell
```

6. Install python packages (using pipenv)

```shell
pipenv install --python 3.13
```
7. Select Python interpreter if using an IDE.
8. Create dummy database

```shell
python -m server.database.setup
```

##### Working with CORS

If the frontend you created runs on a different port than `:8000` or `:8080` (which it should because the API server runs on 8000
or 8080).
Or if the frontend runs on a different URL than `http://localhost/` (in case of deployment).
You should update the `cors.py` file in `server/api/middleware/` folder.

Update this part with your new URL:

```py
origins = [
    "http://localhost",
    "http://localhost:8080",
]
```

##### Working with dev packages

When you want to continue working on the sever side of the project you have to install the dev packages like this:

```shell
pipenv install --dev
```

This installs the packages used when developing:

- graphviz
- eralchemy2
- httpx
- pytest

The pygraphviz and eralchemy2 packages (used for creating ERDiagrams of the SQLAlchemy ORM tables) might show some
trouble because they need GraphViz globally installed on your machine. For iOS users follow these steps:

1. Install graphviz globally using homebrew

```shell
brew install graphviz
```

2. Run this in your virtual env.

- Intel

```shell
CFLAGS="-I/usr/local/include/" LDFLAGS="-L/usr/local/lib/" pip install pygraphviz
```

- Silicon

```shell
CFLAGS="-I/opt/homebrew/include/" LDFLAGS="-L/opt/homebrew/lib/" pip install pygraphviz
```

3. install dev packaged

```shell
pipenv install --dev
```

4. Create ERD

```shell
python -m server.database.create_erd
```

## Usage

1. Run API sever (without debugging)

```shell
fastapi dev server/api/main.py
```
Run API server (with debugging)

```shell
python -m server.api.main
```

2. Go to API docs

```url
http://127.0.0.1:8000/docs
```

## Contributing

## Testing

### Server

Testing on the server side is done with pytest. All API endpoints have happy and unhappy paths.
The tests reside in their own directory. The path is `server/api/tests`. There are no specific tests written for the
database tables.

- To run all pytests:

```shell
pytest
```

- To run specific file:

```shell
pytest server/api/tests/<filename>
```

- To run specific tests:

```shell
pytest -k <function_name>
```

## Changelog

## License

## Acknowledgments