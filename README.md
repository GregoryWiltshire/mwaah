# AWS MWAA Helper (Managed Workflows for Apache Airflow) - Python
Python Client for running Apache Airflow CLI commands on AWS MWAA (Managed Workflows for Apache Airflow) instances.  
Built to give a client like experience for MWAA, utilizing the Apache Python Client objects.

https://docs.aws.amazon.com/mwaa/latest/userguide/airflow-cli-command-reference.html

# (currently) Supported Apache Airflow CLI commands
| Version | Command                  | API         | 
|---------|--------------------------|-------------|
| v2.2.2  | dags list                | get_dags    |
| v2.0+   | dags pause               | pause_dag   |
| v2.0+   | dags unpause             | unpause_dag |
| v2.0+   | dags show                | show_dag    |
| v2.0+   | dags state               | get_dag_state|
| v2.0+   | dags trigger             | new_dagrun  |
| v2.0+   | version                  | get_version |


# Examples
## Running CLI on a private VPC instance
Test locally using the following ssh tunnel configuration  
```shell
ssh -D 8080 -C -N  user@example.com
```
Create a client with proxy config session  
```python
from mwaah import MWAAH

cli = MWAAH(
    'example-mwaa-environment',
    boto3.client('mwaa'),
    proxies={'https': 'socks5://0:8080'}
)
```

## Setting up a new CLI session
Create a client passing in your own session  
```python
from mwaah import MWAAH
cli = MWAAH(
    'example-mwaa-environment',
    boto3.client('mwaa', region_name='example-region-1')
)
```

## Get Version
```python
print(cli.get_version())
```
```
2.2.2
```

## Triggering a New DAG Run
```python
from airflow_client.client.model.dag_run import DAGRun
from dateteim import datetime

date = datetime.now()
run = DAGRun()._from_openapi_data(
    dag_id='example_dag_id',
    execution_date=date,
    dag_run_id="dag_run_id_example"+date.__str__(),
    conf={'key': 'val'},
)
cli.new_dagrun(run)
```
