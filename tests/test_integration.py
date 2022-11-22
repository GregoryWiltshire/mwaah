import os
import time
from datetime import datetime

import boto3
import pytest
from airflow_client.client.model.dag_run import DAGRun
from dotenv import load_dotenv

from MWAAH import MWAAH

dag_list = None
load_dotenv()


@pytest.fixture
def cli() -> MWAAH:
    return MWAAH(
        os.environ['MWAA_ENVIRONMENT_NAME'],
        boto3.client('mwaa'), proxies={'https': 'socks5://0:8080'}
    )


@pytest.fixture
def dag_id() -> str:
    return os.environ["DAG_ID"]


@pytest.fixture
def dag_run(dag_id) -> str:
    date = datetime.now()
    return DAGRun()._from_openapi_data(
        dag_id=dag_id,
        execution_date=date,
        dag_run_id="dag_run_id_example"+date.__str__(),
        conf={'key': 'val'},
    )


@pytest.mark.integration
def test_new_dagrun(cli: MWAAH, dag_run):
    cli.new_dagrun(dag_run)


@pytest.mark.integration
def test_pause_unpause_get_dags(cli: MWAAH, dag_id):
    cli.pause_dag(dag_id)
    dags = [dag for dag in cli.get_dags().__root__ if dag.dag_id == dag_id]
    assert dags[0].paused is True
    cli.unpause_dag(dag_id)
    time.sleep(2)
    dags = [dag for dag in cli.get_dags().__root__ if dag.dag_id == dag_id]
    assert dags[0].paused is False
    cli.pause_dag(dag_id)


@pytest.mark.integration
def test_get_version(cli: MWAAH):
    assert cli.get_version() == '2.2.2'


@pytest.mark.integration
def test_show_dag(cli: MWAAH, dag_id):
    dot = cli.show_dag(dag_id)
    assert dot.startswith(f'digraph {dag_id}')
    assert dot.endswith('}')


@pytest.mark.integration
def test_get_dag_state(cli: MWAAH, dag_run):
    state = cli.get_dag_state(dag_run.dag_id, dag_run.execution_date)
    print(state)


@pytest.mark.integration
def test_get_dag_state_None(cli: MWAAH, dag_run):
    state = cli.get_dag_state(dag_run.dag_id, datetime.now())
    assert state is None


@pytest.mark.slow
@pytest.mark.integration
def test_token_refreshes(cli: MWAAH):
    cli.get_version()
    time.sleep(62.0)  # expires @ 60s
    cli.get_version()
