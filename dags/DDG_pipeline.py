from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "operational_analyst",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    "ddg_operational_pipeline",
    default_args=default_args,
    schedule_interval="@once", 
    catchup=False
) as dag:

    task_fetch = BashOperator(
        task_id="fetch_data",
        bash_command="python /opt/airflow/dags/scripts/fetch_operational_data.py",
    )

    task_process = BashOperator(
        task_id="process_operational",
        bash_command="python /opt/airflow/dags/scripts/process_operational.py",
    )

    task_fetch >> task_process