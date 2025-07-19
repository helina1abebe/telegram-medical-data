from dagster import Definitions
from ethio_pipeline.jobs.etl_job import etl_pipeline_job
from ethio_pipeline.schedules.daily_schedule import daily_etl_schedule

defs = Definitions(
    jobs=[etl_pipeline_job],
    schedules=[daily_etl_schedule]
)
