# DAG example using the SSH operator

import os

from datetime import datetime

from airflow import DAG
from airflow.operators.subdag_operator import SubDagOperator
from airflow.contrib.operators.ssh_operator import SSHOperator

from example_subdag import example_subdag


ETL_HOST = os.environ.get("ETL_HOST")

default_args = {
    'start_date': datetime(2018, 1, 1),
    'retries': 1,
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    schedule_interval='0 1 * * * ',
    catchup=False)

task_one = SSHOperator(
    task_id='task_one',
    ssh_conn_id='private_key',
    remote_host=ETL_HOST,
    command='command for task one {{ params.task_one_param }}',
    params={
        'task_one_param': 1
    },
    dag=dag)

subdag = SubDagOperator(
    subdag=example_subdag(
        'example_dag', 'example_subdag', default_args=default_args,
        schedule_interval=dag.schedule_interval, catchup=dag.catchup),
    task_id='subdag',
    dag=dag)

task_one >> subdag
