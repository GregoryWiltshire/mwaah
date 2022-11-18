import pytest
from dotenv import load_dotenv
import os
import boto3
from mwaacli.mwaa import MWAACLI
from airflow_client.client.model.dag_run import DAGRun
from datetime import datetime


@pytest.fixture
def cli() -> MWAACLI:
    load_dotenv()
    print(os.environ['AWS_DEFAULT_REGION'])
    return MWAACLI(os.environ['MWAA_ENVIRONMENT_NAME'], boto3.client('mwaa'))

def test_get_dags(cli: MWAACLI):
    print(cli.get_dags())


def test_new_dagrun(cli: MWAACLI):
    date = datetime.now()
    run = DAGRun()._from_openapi_data(
        dag_id=os.environ["DAG_ID"],
        execution_date=date,
        dag_run_id="dag_run_id_example"+date.__str__(),
        conf={'key':'val'},
    )
    print(cli.new_dagrun(run))
