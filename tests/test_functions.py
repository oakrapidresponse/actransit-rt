import pathlib

import flask
from functions_framework import create_app


def test_hello() -> None:
    app = create_app("hello", pathlib.Path("src/actransit_rt/functions/main.py"))
    app.testing = True  # bubble exceptions
    client = app.test_client()
    res: flask.response = client.post("/", json={"name": "actransit"})
    assert res.status_code == 200
    assert res.data == b"Hello actransit!"
