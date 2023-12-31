#!/usr/bin/env python3

"""
AC Transit Realtime Archiver

Example usage:
    poetry run actransit-rt version

"""
import os
import pathlib
from collections.abc import Callable

import click
import cloudpathlib
import dotenv
import smart_open

from .functions import gtfs


def _cloud_path(
    ctx: click.Context, param: click.Parameter, value: str
) -> cloudpathlib.CloudPath | pathlib.Path | None:
    """Parameter callback for click to transform str into local or cloud path."""
    if not value:
        return None

    if value.startswith("gs://"):
        return cloudpathlib.GSPath(value)
    else:
        return pathlib.Path(value)


def _output_option() -> Callable:
    return click.option(
        "--output",
        type=str,
        callback=_cloud_path,
    )


def _api_token_option() -> Callable:
    return click.option(
        "--api-token",
        default=lambda: os.environ.get("ACTRANSIT_API_TOKEN", ""),
        show_default="ACTRANSIT_API_TOKEN",
    )


@click.group()
def cli() -> None:
    """Run cli commands"""
    dotenv.load_dotenv()


@cli.command()
def version() -> None:
    """Get the cli version."""
    click.echo(click.style("0.1.0", bold=True))


@cli.command()
@_api_token_option()
@_output_option()
def tripupdates(api_token: str, output: str | None) -> None:
    """Return trip updates feed."""
    feed = gtfs.retrieve_tripupdates_feed(token=api_token)

    if output:
        feed_bytes: str = feed.SerializeToString()
        with smart_open.open(str(output), "wb") as fout:
            fout.write(feed_bytes)
    else:
        click.echo(feed)


@cli.command()
@_api_token_option()
@_output_option()
def vehicles(api_token: str, output: str | None) -> None:
    """Return vehicles feed."""
    feed = gtfs.retrieve_vehicles_feed(token=api_token)

    if output:
        feed_bytes: str = feed.SerializeToString()
        with smart_open.open(str(output), "wb") as fout:
            fout.write(feed_bytes)
    else:
        click.echo(feed)


@cli.command()
@_api_token_option()
@_output_option()
def alerts(api_token: str, output: str | None) -> None:
    """Return alerts feed."""
    feed = gtfs.retrieve_alerts_feed(token=api_token)

    if output:
        feed_bytes: str = feed.SerializeToString()
        with smart_open.open(str(output), "wb") as fout:
            fout.write(feed_bytes)
    else:
        click.echo(feed)


if __name__ == "__main__":
    cli()
