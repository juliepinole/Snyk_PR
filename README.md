# npm dependency server

A web server that provides a basic HTTP api for querying the dependency
tree of a [npm](https://npmjs.org) package.

## Prerequisites

* [Python 3.11](https://www.python.org/downloads/release/python-3116/)

## Getting Started

To install dependencies and start the server in development mode:

```sh
poetry install
poetry run ./manage.py runserver
```

The server will now be running on an available port (defaulting to 8000) and
will restart on changes to the src files.

Then we can try the `/package` endpoint. Here is an example that uses `curl` and
`jq`, but feel free to use any client.

```sh
curl -s http://localhost:8000/package/react/16.13.0 | jq .
```

Most of the code is boilerplate; the logic for the `/package` endpoint can be
found in [src/package.py](src/package.py), and some basic tests in
[test/test_package.py](test/test_package.py)

You can run the tests with:

```sh
poetry run pytest
```

The code is linted using `pre-commit`, you can run this via:

```sh
pre-commit
```
