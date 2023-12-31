import os

import cloudpathlib
import flask
import functions_framework

from . import archive


@functions_framework.http
def hello(request: flask.Request) -> flask.typing.ResponseReturnValue:
    data = request.json or {}
    name = data.get("name", "world")

    return f"Hello {name}!"


@functions_framework.http
def snapshot_feeds(request: flask.Request) -> flask.typing.ResponseReturnValue:
    data = request.json or {}
    is_dryrun = str(data.get("dryrun", "false")).lower() == "true"

    api_token = os.environ.get("ACTRANSIT_API_TOKEN")
    if not api_token:
        print("Must configure a valid ACTRANSIT_API_TOKEN")
        return "Bad config"

    output_dir = os.environ.get("OUTPUT_DIR")
    if not output_dir:
        print("Must configure a valid OUTPUT_DIR")
        return "Bad config"

    try:
        output_path = cloudpathlib.GSPath(output_dir)
    except cloudpathlib.exceptions.CloudPathException:
        print("Must configure a valid gs:// OUTPUT_DIR")
        return "Bad config"

    archive.snapshot_feeds(
        api_token=api_token, output_dir=output_path, is_dryrun=is_dryrun
    )

    return "Success"
