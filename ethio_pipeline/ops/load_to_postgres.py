from dagster import op
import subprocess

@op
def load_raw_to_postgres():
    subprocess.run(["python", "scripts/load_to_postgres.py"], check=True)
