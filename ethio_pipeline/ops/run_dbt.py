from dagster import op
import subprocess

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "transform"], check=True)
