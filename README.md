# monster-compendium

## To install python packages (using pipenv)

```shell
pipenv install
```

> [!NOTE]
> Don't forget to select the python interpreter.

## Run to initialize database

```shell
python -m server.database.setup
```

## Run to start api server

```shell
fastapi dev server/api/main.py
```

## To work with dev packages

pygraphviz sometime gives some trouble on mac intel and mac silicon.
If you want to install the dev packages to create a new ERD follow these steps.

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
