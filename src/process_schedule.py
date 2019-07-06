import os
import pendulum
import pandas as pd
from pandas import read_csv
from analyzer.calendar import Calendar
from analyzer.schedule import scheduleTimeToDateTime

def process_schedule(ctx, datetime):
    agency = ctx.config["metro_agency"]
    start_date = datetime.in_tz(ctx.config["timezone"]).format("YYYY-MM-DD")

    # Load all data
    full_schedule = read_csv("data/GTFS/stop_times.txt")
    calendar = Calendar("data/GTFS/calendar.txt")
    trips = read_csv("data/GTFS/trips.txt")

    # pre-processing (operations on full datasets)
    services_running_today = calendar.services_running_on(start_date).service_id
    trips_running_today = trips[trips["service_id"].isin(services_running_today)]
    trips_and_directions = trips_running_today[["trip_id", "direction_id"]]

    for line_no in range(801, 807):
        line_trips = trips_running_today[trips_running_today["route_id"] == line_no]
        line_schedule = full_schedule[full_schedule["trip_id"].isin(line_trips["trip_id"])]
        line_schedule = scheduleTimeToDateTime(line_schedule, start_date)
        line_schedule = pd.merge(line_schedule, trips_and_directions, on="trip_id")
        line_schedule = line_schedule.drop_duplicates(
            subset=["datetime", "stop_id", "stop_sequence", "direction_id"]
        )
        line_schedule = line_schedule[
            ["datetime", "trip_id", "stop_id", "stop_sequence", "direction_id"]
        ]
        ctx.datastore.write(f"schedule/{line_no}_{agency}/{start_date}.csv", line_schedule.to_csv())

    return "Successfully processed GTFS schedule data and saved line schedules"
