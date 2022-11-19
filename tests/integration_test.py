import os
import time
from datetime import datetime

import boto3
import pytest
from airflow_client.client.model.dag_run import DAGRun
from dotenv import load_dotenv

from mwaacli.mwaa import MWAACLI

dag_list = None
load_dotenv()


@pytest.fixture
def cli() -> MWAACLI:
    return MWAACLI(
        os.environ['MWAA_ENVIRONMENT_NAME'],
        boto3.client('mwaa'), proxies={'https': 'socks5://0:8080'}
    )


@pytest.fixture
def dag_id() -> str:
    return os.environ["DAG_ID"]


def test_new_dagrun(cli: MWAACLI, dag_id):
    date = datetime.now()
    run = DAGRun()._from_openapi_data(
        dag_id=dag_id,
        execution_date=date,
        dag_run_id="dag_run_id_example"+date.__str__(),
        conf={'key': 'val'},
    )
    cli.new_dagrun(run)


def test_pause_unpause_get_dags(cli: MWAACLI, dag_id):
    dags = [dag for dag in cli.get_dags().__root__ if dag.dag_id == dag_id]
    assert dags[0].paused
    cli.unpause_dag(dag_id)
    time.sleep(2)
    dags = [dag for dag in cli.get_dags().__root__ if dag.dag_id == dag_id]
    assert dags[0].paused
    cli.pause_dag(dag_id)


def test_get_version(cli: MWAACLI):
    assert cli.get_version() == '2.2.2'


def test_show_dag(cli: MWAACLI, dag_id):
    dot = cli.show_dag(dag_id)
    assert dot.startswith(f'digraph {dag_id}')
    assert dot.endswith('}')


def test_token_refreshes(cli: MWAACLI):
    cli.get_version()
    time.sleep(62.0)  # expires @ 60s
    cli.get_version()
