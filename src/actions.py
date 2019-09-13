from library import (get_vehicles,
        preprocess_vehicles,
        upload_preprocessed,
        get_schedule,
        process_schedule,
        upload_schedule,
        process_vehicles)

ACTIONS = {
    'GET_VEHICLES': lambda ctx, dt: get_vehicles(ctx),
    'PREPROCESS_VEHICLES': lambda ctx, dt: preprocess_vehicles(ctx),
    'UPLOAD_PREPROCESSED': lambda ctx, dt: upload_preprocessed(ctx),
    'PROCESS_VEHICLES': process_vehicles,
    'GET_SCHEDULE': lambda ctx, dt: get_schedule(ctx),
    'PROCESS_SCHEDULE': process_schedule,
    'UPLOAD_SCHEDULE': upload_schedule
}
