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

### Production

Not yet in production

### Development

#### Server

For a quick start using the server in full capacity you can run the following automated script `./scripts/project_setup.sh`.
This will:

- Install and pipenv (if not yet on machine) and install all dependencies needed for the application.
- Copy the .env.example file to a .env file.
- Create a secret key in the .env file (Windows users have to copy the key from the stdout where it is printed).

##### Manual steps

If the automated script is not working to your liking please follow the manual steps below.

1. Copy the `.env.example` file and name it `.env`
2. Create a random string in a python shell in your terminal or CMD

   - `python` or `python3`
   - `import string`
   - `import random`
   - `print(str(''.join(random.choices(string.ascii_letters,k=82))))`

3. Instal pipenv `pip install --user pipenv`
4. Install python packages (using pipenv)

```shell
pipenv install
```

5. Create pipenv shell

```shell
pipenv shell
```

> [!NOTE]
> Don't forget to select the python interpreter in your IDE.

6. Initialize dummy database

```shell
python -m server.database.setup
```

7. Run API sever (without debugging)

```shell
fastapi dev server/api/main.py
```

###### Optional

1. RUN API server (without debugging)

```shell
python -m server.api.main
```

2. Go to API docs

```url
http://127.0.0.1:8000/docs
```

##### Working with CORS

If the frontend you created runs on a different port than `:8000` (which it should because this API server runs on 8000) or 8080.
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

The pygraphviz and eralchemy2 packages (used for creating ERDiagrams of the SQLAlchemy ORM tables) might show some trouble because they need GraphViz globally installed on your machine. For OS users follow these steps:

1. Install graphviz globally using homebrew

```shell
brew install graphviz
```

2. Run the this in your virtual env.

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

## Contributing

## Testing

## Changelog

## License

## Acknowledgments
