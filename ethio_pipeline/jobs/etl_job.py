from dagster import job
from ethio_pipeline.ops.scrape_telegram import scrape_telegram_data
from ethio_pipeline.ops.load_to_postgres import load_raw_to_postgres
from ethio_pipeline.ops.run_dbt import run_dbt_transformations
from ethio_pipeline.ops.run_yolo import run_yolo_enrichment

@job
def etl_pipeline_job():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
