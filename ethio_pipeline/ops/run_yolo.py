from dagster import op
import subprocess

@op
def run_yolo_enrichment():
    subprocess.run(["python", "scripts/run_yolo.py"], check=True)
