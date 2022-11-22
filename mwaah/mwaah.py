import base64
import json
from datetime import datetime, timedelta
from typing import Union

import boto3
import requests
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.dag_state import DagState

from .model import DagList


class MWAAData:
    def __init__(self, resp):
        self.stdout = base64.b64decode(
            resp.json()['stdout']
        ).decode('utf8').strip()
        self.stderr = base64.b64decode(
            resp.json()['stderr']
        ).decode('utf8').strip()
        self.raw_stdout = base64.b64decode(resp.json()['stdout']).decode('utf8')
        if 'airflow.exceptions' in self.stderr:
            raise Exception(self.stderr)

    def json(self) -> dict:
        return json.loads(self.stdout)


class MWAAH:
    def __init__(self, name, mwaa_client=None, proxies=None):
        if mwaa_client:
            self.client = mwaa_client
        else:
            self.client = boto3.client('mwaa')
        self.name = name
        self.proxies = proxies
        self.__token_expiration__ = None
        self.__token__ = None

    def get_token(self) -> dict:
        if self.__token__:
            if self.__token_expiration__ > datetime.now():
                return self.__token__
        self.__token__ = self.client.create_cli_token(Name=self.name)
        self.__token_expiration__ = datetime.now() + timedelta(minutes=1)
        return self.__token__

    def post_command(self, cmd: str) -> MWAAData:
        host = f"""https://{self.get_token()['WebServerHostname']}/aws_mwaa/cli"""
        resp = requests.post(
            host,
            headers={
                'Authorization': 'Bearer ' + self.get_token()['CliToken'],
                'Content-Type': 'text/plain'
            },
            proxies=self.proxies,
            data=cmd,
            timeout=60
        )
        resp.raise_for_status()
        return MWAAData(resp)

    def get_dags(self) -> DagList:
        data = self.post_command('dags list --output json')
        return DagList(__root__=data.json())

    def new_dagrun(self, dag_run: DAGRun):
        cmd = 'dags trigger'
        if dag_run.get('conf'):
            cmd += f""" --conf '{json.dumps(dag_run.conf)}'"""
        if dag_run.get('execution_date'):
            cmd += f""" --exec-date '{dag_run.execution_date}'"""
        if dag_run.get('dag_run_id'):
            cmd += f""" --run-id '{dag_run.dag_run_id}'"""
        cmd += f""" '{dag_run.dag_id}'"""
        self.post_command(cmd)

    def get_dag_state(self, dag_id: str, execution_date: datetime) -> Union[DagState, None]:
        data = self.post_command(
            """dags state '{}' '{}'""".format(dag_id, execution_date.isoformat())
        )
        state_str = data.raw_stdout.split('\x1b[0m')[-1].strip()
        if state_str == 'None':
            return None
        return DagState(state_str)

    def pause_dag(self, dag_id: str):
        self.post_command("""dags pause '{}'""".format(dag_id))

    def unpause_dag(self, dag_id: str):
        self.post_command("""dags unpause '{}'""".format(dag_id))

    def get_version(self) -> str:
        return self.post_command('version').stdout

    # returns DOT representation of DAG
    def show_dag(self, dag_id) -> str:
        raw_str = self.post_command("""dags show '{}'""".format(dag_id)).raw_stdout
        return raw_str.split('\x1b[0m')[4].strip()  # split by control code, whitespace
