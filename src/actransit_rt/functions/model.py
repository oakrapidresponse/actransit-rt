"""
https:#github.com/MobilityData/gtfs-realtime-bindings/blob/master/gtfs-realtime.proto
"""

import dataclasses
import datetime
import enum

import pendulum
from google.transit import gtfs_realtime_pb2


class TripScheduleRelationship(enum.IntEnum):
    """Enum for vehicle schedule relationship"""

    # Trip that is running in accordance with its GTFS schedule, or is close
    # enough to the scheduled trip to be associated with it.
    SCHEDULED = 0

    # An extra trip that was added in addition to a running schedule, for
    # example, to replace a broken vehicle or to respond to sudden passenger
    # load.
    ADDED = 1

    # A trip that is running with no schedule associated to it (GTFS frequencies.txt exact_times=0).
    # Trips with ScheduleRelationship=UNSCHEDULED must also set all StopTimeUpdates.ScheduleRelationship=UNSCHEDULED.
    UNSCHEDULED = 2

    # A trip that existed in the schedule but was removed.
    CANCELED = 3

    # Should not be used - for backwards-compatibility only.
    REPLACEMENT = 5

    # An extra trip that was added in addition to a running schedule, for example, to replace a broken vehicle or to
    # respond to sudden passenger load.
    DUPLICATED = 6


class VehicleStopStatus(enum.IntEnum):
    """Enum for vehicle status"""

    # The vehicle is just about to arrive at the stop (on a stop
    # display, the vehicle symbol typically flashes).
    INCOMING_AT = 0

    # The vehicle is standing at the stop.
    STOPPED_AT = 1

    # The vehicle has departed and is in transit to the next stop.
    IN_TRANSIT_TO = 2


class VehicleCongestionLevel(enum.IntEnum):
    """Enum for vehicle congestion level"""

    UNKNOWN_CONGESTION_LEVEL = 0
    RUNNING_SMOOTHLY = 1
    STOP_AND_GO = 2
    CONGESTION = 3
    SEVERE_CONGESTION = 4


class VehicleOccupancyStatus(enum.IntEnum):
    """Enum for vehicle occupancy status"""

    # The vehicle or carriage is considered empty by most measures, and has few or no
    # passengers onboard, but is still accepting passengers.
    EMPTY = 0

    # The vehicle or carriage has a relatively large percentage of seats available.
    MANY_SEATS_AVAILABLE = 1

    # The vehicle or carriage has a relatively small percentage of seats available.
    FEW_SEATS_AVAILABLE = 2

    # The vehicle or carriage can currently accommodate only standing passengers.
    STANDING_ROOM_ONLY = 3

    # The vehicle or carriage can currently accommodate only standing passengers
    # and has limited space for them.
    CRUSHED_STANDING_ROOM_ONLY = 4

    # The vehicle or carriage is considered full by most measures, but may still be
    # allowing passengers to board.
    FULL = 5

    # The vehicle or carriage is not accepting passengers, but usually accepts passengers for boarding.
    NOT_ACCEPTING_PASSENGERS = 6

    # The vehicle or carriage doesn't have any occupancy data available at that time.
    NO_DATA_AVAILABLE = 7

    # The vehicle or carriage is not boardable and never accepts passengers.
    # Useful for special vehicles or carriages (engine, maintenance carriage, etc…).
    NOT_BOARDABLE = 8


@dataclasses.dataclass(frozen=True, kw_only=True)
class VehiclePosition:
    """Data for a GFTS-RT vehicle"""

    # The Trip that this vehicle is serving.
    # Can be empty or partial if the vehicle can not be identified with a given trip instance.
    trip_id: str | None = None
    route_id: str | None = None
    direction_id: int | None = None
    start_datetime: datetime.datetime | None = None
    schedule_relationship: TripScheduleRelationship | None = None

    #  Additional information on the vehicle that is serving this trip.
    vehicle_id: str | None = None
    vehicle_label: str | None = None
    vehicle_license_plate: str | None = None

    #  Current position of this vehicle.
    latitude: float | None = None
    longitude: str | None = None
    bearing: int | None = None
    odometer: float | None = None
    speed: float | None = None

    # The stop sequence index of the current stop.
    current_stop_sequence: int | None = None

    # Identifies the current stop.
    stop_id: str | None = None

    # The exact status of the vehicle with respect to the current stop.
    current_status: VehicleStopStatus | None = None

    # Moment at which the vehicle's position was measured.
    timestamp: datetime.datetime | None = None

    # Congestion level that is affecting this vehicle.
    congestion_level: VehicleCongestionLevel | None = None

    # If multi_carriage_status is populated with per-carriage OccupancyStatus,
    # then this field should describe the entire vehicle with all carriages accepting passengers considered.
    occupancy_status: VehicleOccupancyStatus | None = None

    # A percentage value representing the degree of passenger occupancy of the vehicle.
    # The values are represented as an integer without decimals. 0 means 0% and 100 means 100%.
    # The value 100 should represent the total maximum occupancy the vehicle was designed for,
    # including both seated and standing capacity, and current operating regulations allow.
    occupancy_percentage: int | None = None

    @classmethod
    def from_feed(cls, vehicle: gtfs_realtime_pb2.VehiclePosition) -> "VehiclePosition":
        """Create a VehiclePosition from a feed VehiclePosition"""
        start_datetime = None
        if vehicle.trip.start_date and vehicle.trip.start_time:
            try:
                start_pendulum = pendulum.from_format(
                    f"{vehicle.trip.start_date} {vehicle.trip.start_time}",
                    "YYYYMMDD HH:mm:ss",
                )
                start_datetime = datetime.datetime.fromisoformat(
                    start_pendulum.isoformat()
                )
            except ValueError:
                print(
                    f"Error parsing {vehicle.trip.start_date} {vehicle.trip.start_time}"
                )

        return VehiclePosition(
            # Trip
            trip_id=vehicle.trip.trip_id if vehicle.trip.trip_id else None,
            route_id=vehicle.trip.route_id if vehicle.trip.route_id else None,
            direction_id=(
                vehicle.trip.direction_id if vehicle.trip.direction_id else None
            ),
            start_datetime=start_datetime,
            schedule_relationship=TripScheduleRelationship(
                vehicle.trip.schedule_relationship
            ),
            # Vehicle
            vehicle_id=vehicle.vehicle.id,
            vehicle_label=vehicle.vehicle.label,
            vehicle_license_plate=vehicle.vehicle.license_plate,
            # Position
            latitude=vehicle.position.latitude,
            longitude=vehicle.position.longitude,
            bearing=vehicle.position.bearing,
            odometer=vehicle.position.odometer,
            speed=vehicle.position.speed,
            # ...
            current_stop_sequence=vehicle.current_stop_sequence,
            stop_id=vehicle.stop_id if vehicle.stop_id else None,
            current_status=VehicleStopStatus(vehicle.current_status),
            timestamp=datetime.datetime.fromtimestamp(
                vehicle.timestamp, tz=pendulum.UTC
            ),
            congestion_level=(
                VehicleCongestionLevel(vehicle.congestion_level)
                if vehicle.congestion_level
                else None
            ),
            occupancy_status=(
                VehicleOccupancyStatus(vehicle.occupancy_status)
                if vehicle.occupancy_status
                else None
            ),
            occupancy_percentage=vehicle.occupancy_percentage,
        )
