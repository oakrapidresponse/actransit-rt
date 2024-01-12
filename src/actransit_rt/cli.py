#!/usr/bin/env python3

"""
AC Transit Realtime Archiver

Example usage:
    poetry run actransit-rt version

"""
import os
import pathlib
from collections.abc import Callable
from typing import TypeAlias

import click
import cloudpathlib
import dotenv
import smart_open

from .functions import archive, gtfs

APath: TypeAlias = cloudpathlib.CloudPath | pathlib.Path


def _cloud_path(ctx: click.Context, param: click.Parameter, value: str) -> APath | None:
    """Parameter callback for click to transform str into local or cloud path."""
    if not value:
        return None

    return cloudpathlib.anypath.to_anypath(value)


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


def _dry_run_option() -> Callable:
    return click.option("--dry-run/--no-dry-run", type=bool, default=False)


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
@click.option(
    "--output-dir",
    type=str,
    callback=_cloud_path,
    required=True,
)
@_dry_run_option()
def snapshot(api_token: str, output_dir: APath, dry_run: bool) -> None:
    """Snapshot and archive all realtime feeds."""
    archive.snapshot_all(api_token=api_token, output_dir=output_dir, is_dryrun=dry_run)


@cli.group("api")
def api_group() -> None:
    """Run api commands"""
    pass


@api_group.command(name="tripupdates")
@_api_token_option()
@_output_option()
def api_tripupdates(api_token: str, output: APath | None) -> None:
    """Return trip updates feed."""
    feed = gtfs.retrieve_tripupdates_feed(token=api_token)

    if output:
        feed_bytes: str = feed.SerializeToString()
        with smart_open.open(str(output), "wb") as fout:
            fout.write(feed_bytes)
    else:
        click.echo(feed)


@api_group.command(name="vehicles")
@_api_token_option()
@_output_option()
def api_vehicles(api_token: str, output: APath | None) -> None:
    """Return vehicles feed."""
    feed = gtfs.retrieve_vehicles_feed(token=api_token)

    if output:
        feed_bytes: str = feed.SerializeToString()
        with smart_open.open(str(output), "wb") as fout:
            fout.write(feed_bytes)
    else:
        click.echo(feed)


@api_group.command(name="alerts")
@_api_token_option()
@_output_option()
def api_alerts(api_token: str, output: APath | None) -> None:
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
