# This file is managed by the 'airflow' file bundle and updated automatically when `meltano upgrade` is run.
# To prevent any manual changes from being overwritten, remove the file bundle from `meltano.yml` or disable automatic updates:
#     meltano config --plugin-type=files airflow set _update orchestrate/dags/meltano.py false

# If you want to define a custom DAG, create
# a new file under orchestrate/dags/ and Airflow
# will pick it up automatically.

import os
import logging
import subprocess
import json

from airflow import DAG
from airflow.utils import timezone
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta
from pathlib import Path


logger = logging.getLogger(__name__)


DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": timezone.parse("2023-12-10", "Europe/Paris"),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "catchup": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "concurrency": 1,
}

project_root = os.getenv("MELTANO_PROJECT_ROOT", os.getcwd())

meltano_bin = ".meltano/run/bin"

if not Path(project_root).joinpath(meltano_bin).exists():
    logger.warning(f"A symlink to the 'meltano' executable could not be found at '{meltano_bin}'. Falling back on expecting it to be in the PATH instead.")
    meltano_bin = "meltano"


with DAG(
        "meltano_spacexapi_daily",
        catchup=False,
        default_args=DEFAULT_ARGS,
        schedule_interval="@daily",
        max_active_runs=1,
) as dag:

    extract_load = BashOperator(
        task_id="extract_load",
        bash_command=f"cd {project_root}; {meltano_bin} elt tap-spacexapi target-postgres",
        env={
            # inherit the current env
            **os.environ,
        },
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=f"cd {project_root}; {meltano_bin} invoke dbt-postgres:run",
        env={
            # inherit the current env
            **os.environ,
        },
    )

    end_task = DummyOperator(task_id="end_of_dag")

    extract_load >> transform >> end_task

    


