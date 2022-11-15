import boto3
import json
import requests
import base64
from model import DagList
from airflow_client.client.model.dag_run import DAGRun
from datetime import datetime
import re

class MWAAData:
    def __init__(self, resp):
        self.stdout = base64.b64decode(resp.json()['stdout']).decode('utf8')
        self.stderr = base64.b64decode(resp.json()['stderr']).decode('utf8')
        if 'airflow.exceptions' in self.stderr:
            raise Exception(self.stderr)
    def json(self) -> dict:
        return json.loads(self.stdout)

class MWAACLI:
    def __init__(self, name, client=boto3.client('mwaa')):
        self.client = client
        self.name = name
        self.token = self.get_token()

    def get_token(self) -> dict:
        return self.client.create_cli_token(Name=self.name)

    def post_command(self, cmd: str) -> MWAAData:
        host = f"""https://{self.token['WebServerHostname']}/aws_mwaa/cli"""
        resp = requests.post(
            host,
            headers={
            'Authorization': 'Bearer ' + self.token['CliToken'],
            'Content-Type': 'text/plain'
            },
            proxies={'https': 'socks5://0:8080'},
            data=cmd,
            timeout=60
        )
        resp.raise_for_status()
        return MWAAData(resp)
    
    def get_dags(self) -> DagList:
        data = self.post_command('dags list --output json')
        return DagList(__root__=data.json())
    
    def new_dagrun(self, dag_run :DAGRun) -> DAGRun:
        cmd = 'dags trigger'
        if dag_run.conf:
            cmd += f""" --conf '{json.dumps(dag_run.conf)}'"""
        if dag_run.get('execution_date'):
            cmd += f""" --exec-date '{dag_run.execution_date}'"""
        if dag_run.dag_run_id:
            cmd += f""" --run-id '{dag_run.dag_run_id}'"""
        cmd += f""" '{dag_run.dag_id}'"""
        data = self.post_command(cmd)
        # return data
        regexp = r'(?m)(?:.+\nCreated <DagRun )([a-zA-Z0-9\-\_.]+) @ ([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}): (.+), externally triggered: (True|False)>'
        r = re.compile(regexp)
        _, execution_date, dag_run_id, externally_triggered = r.findall(data.stdout)[0]
        execution_date = datetime.fromisoformat(execution_date)
        return DAGRun()._new_from_openapi_data(
            **{**dag_run.to_dict(), **{'execution_date': execution_date, 'externally_triggered': externally_triggered}}
        )
