# App Structure

This app is a set of scripts that need to be run at various frequencies according to their file names. These scripts live in the tasks folder and invoke the following actions via main.py through importing files in the library folder:

## Schedule:

-- old --

Every Minute:
- Get current vehicle positions and save to raw json documents:
    script: query_vehicles.sh
- Get current predictions and save to raw json documents (disabled by default for disk space)z:
    script: query_predictions.sh
    
Every 30 Minutes:
- Process vehicles (get relative_position, datetime, trip_id and direction), produce estimated arrival times for each trip, optionally upload:
    script: process_vehicles.sh (or process_upload_vehicles.sh)

Daily (2-3am):
- Get current schedule, process and (optionally) upload to S3:
    script: query_schedule.sh (or upload_schedule.sh)

Once Only (unless new stops are added in future) [obsolete, these files just live on the repo now, they don't need to be fetched]:    
- Use schedule to prepare list of unique stops (use with caution, schedule doesn't always include all stops):
    script: prepare_stop_list.sh

-- New --
Every Minute:
- Get current vehicle positions and save to raw json documents:
    action name: GET_VEHICLES
    filename: get_vehicles.py
- 
    action name: PREPROCESS_VEHICLES
    filename: preprocess_vehicles.py

- 
    action name: UPLOAD_PREPROCESSED
    filename: upload_preprocessed.py

Every 15 Minutes (replaces 30 min cycle):

- 
    action name: GET_PREPROCESSED_VEHICLE_DATA
    filename:

- 
    action name: PROCESS_VEHICLE_DATA
    filename:

- 
    action name: ESTIMATE_ARRIVALS
    filename:

- 
    action name: PRODUCE_SUMMARY
    filename:

-
    action name: UPLOAD_SUMMARY
    filename:
-
    action name: UPLOAD_PROCESSED_VEHICLES
    filename:

Daily (2am):
- Get the current schedule for the new day before trips begin.
    action name: GET_SCHEDULE
    filename:
- Process the schedule.
    action name: PROCESS_SCHEDULE
    filename:

-   Upload to S3 or do nothing?
    action name: UPLOAD_SCHEDULE
    filename: 