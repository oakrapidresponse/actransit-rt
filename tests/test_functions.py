import pathlib

import flask
from cloudevents import conversion
from cloudevents.http.event import CloudEvent
from functions_framework import create_app


def test_hello() -> None:
    app = create_app("hello", pathlib.Path("src/actransit_rt/functions/main.py"))
    app.testing = True  # bubble exceptions
    client = app.test_client()
    res: flask.response = client.post("/", json={"name": "actransit"})
    assert res.status_code == 200
    assert res.data == b"Hello actransit!"


def test_ping() -> None:
    app = create_app("ping", pathlib.Path("src/actransit_rt/functions/main.py"))
    app.testing = True  # bubble exceptions
    client = app.test_client()

    event = CloudEvent.create(
        {
            "specversion": "1.0",
            "type": "google.cloud.scheduler.job.v1.execute",
            "source": "https://example.com/cloudevents/pull",
            "subject": "123",
            "id": "A234-1234-1234",
            "time": "2018-04-05T17:31:00Z",
        },
        "hello world",
    )

    res: flask.response = client.post(
        "/",
        json=conversion.to_dict(event),
        headers={"Content-Type": "application/cloudevents+json"},
    )
    assert res.status_code == 200
