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

### To go to API docs

```url
http://127.0.0.1:8000/docs
```

## Working with CORS

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
