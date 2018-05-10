# SubDAG example using the SSH operator

import os

from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

ETL_HOST = os.environ.get("ETL_HOST")


def example_subdag(parent_dag_name, child_dag_name, **kwargs):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name), **kwargs)

    task_one = SSHOperator(
        task_id='task_one',
        ssh_conn_id='private_key',
        remote_host=ETL_HOST,
        command='command for task one {{ params.task_one_param }}',
        params={
            'task_one_param': 1
        },
        dag=dag)

    task_two = SSHOperator(
        task_id='task_two',
        ssh_conn_id='private_key',
        remote_host=ETL_HOST,
        command='command for task two {{ params.task_two_param }}',
        params={
            'task_two_param': 2
        },
        dag=dag)

    task_one >> task_two

    return dag
