#!/usr/bin/env python3

"""
AC Transit Realtime Archiver

Example usage:
    poetry run actransit-rt version

"""
import os
import pathlib
from collections.abc import Callable
from typing import Literal, TypeAlias

import click
import cloudpathlib
import dotenv
import orjson
import pandas as pd
import pendulum
import smart_open

from .functions import archive, gtfs

APath: TypeAlias = cloudpathlib.CloudPath | pathlib.Path


def _cloud_path(ctx: click.Context, param: click.Parameter, value: str) -> APath | None:
    """Parameter callback for click to transform str into local or cloud path."""
    if not value:
        return None

    return cloudpathlib.anypath.to_anypath(value)


def _pendulum_datetime(side: Literal["start"] | Literal["end"] = "start") -> Callable:
    def _callback(
        ctx: click.Context, param: click.Parameter, value: str
    ) -> pendulum.DateTime | None:
        """Parameter callback for click to transform str into pendulum datetime"""
        if not value:
            return None

        parsed = pendulum.parse(value, tz="America/Los_Angeles", exact=True)

        if isinstance(parsed, pendulum.DateTime):
            return parsed

        elif isinstance(parsed, pendulum.Duration):
            raise ValueError("Must specify a date or datetime, not a duration")

        elif isinstance(parsed, pendulum.Time):
            raise ValueError("Must specify a date or datetime, not a time")

        elif isinstance(parsed, pendulum.Date):
            parsed_dt = pendulum.datetime(
                parsed.year, parsed.month, parsed.day, tz="America/Los_Angeles"
            )

            if side == "start":
                return parsed_dt.start_of("day")
            else:
                return parsed_dt.end_of("day")

        return None

    return _callback


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
        show_default="$ACTRANSIT_API_TOKEN",
    )


def _input_dir_option() -> Callable:
    return click.option(
        "--input-dir",
        type=str,
        default=lambda: os.environ.get("INPUT_DIR", ""),
        callback=_cloud_path,
        show_default="$INPUT_DIR",
    )


def _dry_run_option() -> Callable:
    return click.option("--dry-run/--no-dry-run", type=bool, default=False)


def _start_option() -> Callable:
    return click.option(
        "--start",
        type=str,
        callback=_pendulum_datetime("start"),
        default=lambda: pendulum.now("America/Los_Angeles"),
    )


def _end_option() -> Callable:
    return click.option(
        "--end",
        type=str,
        callback=_pendulum_datetime("end"),
        default=lambda: pendulum.now("America/Los_Angeles"),
    )


def _limit_option() -> Callable:
    return click.option(
        "--limit",
        type=int,
        default=10,
    )


def _format_option() -> Callable:
    return click.option(
        "--format",
        type=click.Choice(["jsonl", "csv", "parquet"]),
        default="jsonl",
    )


def _filter_option() -> Callable:
    return click.option(
        "--filter",
        type=str,
        callback=lambda ctx, param, value: dict(
            [v.split(":") for v in value.split(",")]
        ),
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
@click.option(
    "--output-dir",
    type=str,
    callback=_cloud_path,
    default=lambda: os.environ.get("OUTPUT_DIR", ""),
    show_default="$OUTPUT_DIR",
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


@cli.group("archive")
def archive_group() -> None:
    """Run archive commands"""
    pass


@archive_group.command(name="retrieve-tripupdates")
@_input_dir_option()
@_start_option()
@_end_option()
@_limit_option()
def archive_retrieve_tripupdates(
    input_dir: APath, start: pendulum.DateTime, end: pendulum.DateTime, limit: int
) -> None:
    """Display archived trip update feeds."""
    feeds = archive.retrieve_tripupdate_feeds(input_dir, start, end, limit)
    for feed in feeds:
        click.echo(feed)


@archive_group.command(name="retrieve-vehicle-positions")
@_input_dir_option()
@_start_option()
@_end_option()
@_filter_option()
@_limit_option()
@_output_option()
@_format_option()
def archive_retrieve_vehicles(
    input_dir: APath,
    start: pendulum.DateTime,
    end: pendulum.DateTime,
    filter: dict[str, str] | None,
    limit: int | None,
    output: APath | None,
    format: Literal["jsonl"] | Literal["csv"] | Literal["parquet"],
) -> None:
    """Display archived vehicles feeds."""
    vehicles = archive.retrieve_vehicle_positions(input_dir, start, end, filter, limit)

    if output:
        vehicle_df = pd.DataFrame(vehicles)

        with smart_open.open(str(output), "wb") as fout:
            if format == "jsonl":
                vehicle_df.to_json(fout, orient="records", lines=True)

            elif format == "csv":
                vehicle_df.to_csv(fout, index=False)

            elif format == "parquet":
                vehicle_df.to_parquet(fout, index=False)

    else:
        for vehicle in vehicles:
            click.echo(orjson.dumps(vehicle))


@archive_group.command(name="retrieve-alerts")
@_input_dir_option()
@_start_option()
@_end_option()
@_limit_option()
def archive_retrieve_alerts(
    input_dir: APath, start: pendulum.DateTime, end: pendulum.DateTime, limit: int
) -> None:
    """Display archived alert feeds."""
    feeds = archive.retrieve_alert_feeds(input_dir, start, end, limit)
    for feed in feeds:
        click.echo(feed)


if __name__ == "__main__":
    cli()
