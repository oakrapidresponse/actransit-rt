import flask
import functions_framework
from cloudevents.http.event import CloudEvent


@functions_framework.http
def hello(request: flask.Request) -> flask.typing.ResponseReturnValue:
    data = request.json or {}
    name = data.get("name", "world")

    return f"Hello {name}!"


@functions_framework.cloud_event
def ping(cloud_event: CloudEvent) -> None:
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
