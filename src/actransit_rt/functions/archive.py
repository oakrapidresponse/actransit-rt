"""Utilities for storing feeds

/actransit/realtime/tripupdates/2024/02/15/1703994731.tripupdates.pb.gz
/actransit/realtime/alerts/2024/02/15/1703994731.alerts.pb.gz
/actransit/realtime/vehicles/2024/02/15/1703994731.vehicles.pb.gz
"""
import pathlib
from collections.abc import Iterator
from typing import TypeAlias

import cloudpathlib
import pendulum
import smart_open
from google.transit import gtfs_realtime_pb2

from . import gtfs

APath: TypeAlias = cloudpathlib.CloudPath | pathlib.Path


def base_path(kind: str, output_dir: APath, day: pendulum.Date) -> APath:
    return (
        output_dir / kind / day.strftime("%Y") / day.strftime("%m") / day.strftime("%d")
    )


def output_path(kind: str, output_dir: APath, timestamp: int) -> APath:
    day = pendulum.from_timestamp(timestamp, tz="UTC")
    return base_path(kind, output_dir, day) / f"{timestamp}.{kind}.pb.gz"


def snapshot_all(api_token: str, output_dir: APath, is_dryrun: bool = False) -> None:
    snapshot_tripupdates_feed(api_token, output_dir, is_dryrun=is_dryrun)
    snapshot_alerts_feed(api_token, output_dir, is_dryrun=is_dryrun)
    snapshot_vehicles_feed(api_token, output_dir, is_dryrun=is_dryrun)


def snapshot_tripupdates_feed(
    api_token: str, output_dir: APath, is_dryrun: bool = False
) -> None:
    feed = gtfs.retrieve_tripupdates_feed(token=api_token)

    timestamp = int(feed.header.timestamp)

    output = output_path("tripupdates", output_dir, timestamp)

    print(f"Snapshotting {len(feed.entity)} tripupdates to {output}")

    if is_dryrun:
        return

    output.parent.mkdir(parents=True, exist_ok=True)

    feed_bytes: str = feed.SerializeToString()
    with smart_open.open(str(output), "wb") as fout:
        fout.write(feed_bytes)


def snapshot_alerts_feed(
    api_token: str, output_dir: APath, is_dryrun: bool = False
) -> None:
    feed = gtfs.retrieve_alerts_feed(token=api_token)

    timestamp = int(feed.header.timestamp)

    output = output_path("alerts", output_dir, timestamp)

    print(f"Snapshotting {len(feed.entity)} alerts to {output}")

    if is_dryrun:
        return

    output.parent.mkdir(parents=True, exist_ok=True)

    feed_bytes: str = feed.SerializeToString()
    with smart_open.open(str(output), "wb") as fout:
        fout.write(feed_bytes)


def snapshot_vehicles_feed(
    api_token: str, output_dir: APath, is_dryrun: bool = False
) -> None:
    feed = gtfs.retrieve_vehicles_feed(token=api_token)

    timestamp = int(feed.header.timestamp)

    output = output_path("vehicles", output_dir, timestamp)

    print(f"Snapshotting {len(feed.entity)} vehicles to {output}")

    if is_dryrun:
        return

    output.parent.mkdir(parents=True, exist_ok=True)

    feed_bytes: str = feed.SerializeToString()
    with smart_open.open(str(output), "wb") as fout:
        fout.write(feed_bytes)


def retrieve_tripupdate_feeds(
    base_dir: APath, start: pendulum.DateTime, end: pendulum.DateTime
) -> Iterator:
    start_utc = start.in_tz("UTC")
    end_utc = end.in_tz("UTC")

    for day in pendulum.interval(start_utc, end_utc).range("days"):
        output_path = base_path("tripupdates", base_dir, day)
        feed_paths = output_path.glob("*.tripupdates.pb.gz")

        for feed_path in feed_paths:
            with smart_open.open(str(feed_path), "rb") as fin:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(fin.read())

                yield feed


def retrieve_alert_feeds(
    base_dir: APath, start: pendulum.DateTime, end: pendulum.DateTime
) -> Iterator:
    start_utc = start.in_tz("UTC")
    end_utc = end.in_tz("UTC")

    for day in pendulum.interval(start_utc, end_utc).range("days"):
        output_path = base_path("alerts", base_dir, day)
        feed_paths = output_path.glob("*.alerts.pb.gz")

        for feed_path in feed_paths:
            with smart_open.open(str(feed_path), "rb") as fin:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(fin.read())

                yield feed


def retrieve_vehicle_feeds(
    base_dir: APath, start: pendulum.DateTime, end: pendulum.DateTime
) -> Iterator:
    start_utc = start.in_tz("UTC")
    end_utc = end.in_tz("UTC")

    for day in pendulum.interval(start_utc, end_utc).range("days"):
        output_path = base_path("vehicles", base_dir, day)
        feed_paths = output_path.glob("*.vehicles.pb.gz")

        for feed_path in feed_paths:
            with smart_open.open(str(feed_path), "rb") as fin:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(fin.read())

                yield feed
