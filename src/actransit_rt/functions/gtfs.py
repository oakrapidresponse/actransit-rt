"""Libraries for retrieving and processing GTFS"""

import requests
from google.transit import gtfs_realtime_pb2

BASE_URL = "https://api.actransit.org/transit"


def retrieve_tripupdates_feed(token: str) -> gtfs_realtime_pb2.FeedMessage:
    url = f"{BASE_URL}/gtfsrt/tripupdates"
    response = requests.get(url, {"token": token})

    if response.status_code != 200:
        raise RuntimeError(f"Could not access trip updates feed at: {url}")

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    return feed


def retrieve_vehicles_feed(token: str) -> gtfs_realtime_pb2.FeedMessage:
    url = f"{BASE_URL}/gtfsrt/vehicles"
    response = requests.get(url, {"token": token})

    if response.status_code != 200:
        raise RuntimeError(f"Could not access vehicles feed at: {url}")

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    return feed


def retrieve_alerts_feed(token: str) -> gtfs_realtime_pb2.FeedMessage:
    url = f"{BASE_URL}/gtfsrt/alerts"
    response = requests.get(url, {"token": token})

    if response.status_code != 200:
        raise RuntimeError(f"Could not access alerts feed at: {url}")

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    return feed
