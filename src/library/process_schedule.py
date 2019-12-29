import os
import pendulum
import pandas as pd
from .analyzer.calendar import Calendar
from .analyzer.schedule import scheduleTimeToDateTime

def process_schedule(ctx, datetime):
    agency = ctx.config["METRO_AGENCY"]
    lines = ctx.config["METRO_LINES"]
    start_date = datetime.in_tz(ctx.config["TIMEZONE"]).format("YYYY-MM-DD")

    ctx.logger(f"Loading schedule for date {start_date}")
    # Load all data
    try:
        full_schedule = pd.read_csv(ctx.tmp.get_abs_path("GTFS/stop_times.txt"))
        calendar = Calendar(ctx.tmp.get_abs_path("GTFS/calendar.txt"))
        trips = pd.read_csv(ctx.tmp.get_abs_path("GTFS/trips.txt"))
    except:
        ctx.logger("Could not find required data for processing the schedule")
        return 1

    # pre-processing (operations on full datasets)
    services_running_today = calendar.services_running_on(start_date).service_id
    trips_running_today = trips[trips["service_id"].isin(services_running_today)]
    trips_and_directions = trips_running_today[["trip_id", "direction_id"]]

    for line in lines:
        line_trips = trips_running_today[trips_running_today["route_id"] == line]
        line_schedule = full_schedule[full_schedule["trip_id"].isin(line_trips["trip_id"])]
        line_schedule = scheduleTimeToDateTime(line_schedule, start_date)
        line_schedule = pd.merge(line_schedule, trips_and_directions, on="trip_id")
        line_schedule = line_schedule.drop_duplicates(
            subset=["datetime", "stop_id", "stop_sequence", "direction_id"]
        )
        line_schedule = line_schedule[
            ["datetime", "trip_id", "stop_id", "stop_sequence", "direction_id"]
        ]
        storage_path = f"schedule/{agency}/{line}/{start_date}.csv"
        ctx.logger(f"Saving schedule for line {line} and date {start_date}")
        ctx.datastore.write(storage_path, line_schedule.to_csv())

    return 0
