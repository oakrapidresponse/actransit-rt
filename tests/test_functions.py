import pathlib

import flask
from functions_framework import create_app


def test_integration() -> None:
    app = create_app("hello", pathlib.Path("src/actransit_rt/functions/main.py"))
    app.testing = True  # bubble exceptions
    client = app.test_client()
    res: flask.response = client.post("/", json={"hello": "world"})
    assert res.status_code == 200
