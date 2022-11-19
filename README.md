# AWS MWAA (Managed Workflows for Apache Airflow) CLI - Python
Python Client for running Apache Airflow CLI commands on AWS MWAA (Managed Workflows for Apache Airflow) instances.  
https://docs.aws.amazon.com/mwaa/latest/userguide/airflow-cli-command-reference.html

# (currently) Supported Apache Airflow CLI commands
| Version | Command                  | Implemented | Integration Test |
|---------|--------------------------|-------------|------------------|
| v2.2.2  | dags list                |     ✅      |       ✅         |
| v2.0+   | dags pause               |     ✅      |       ✅         |
| v2.0+   | dags unpause             |     ✅      |       ✅         |
| v2.0+   | dags show                |     ✅      |       ✅         |
| v2.0+   | dags state               |     ✅      |       ✅         |
| v2.0+   | dags trigger             |     ✅      |       ✅         |
| v2.0+   | version                  |     ✅      |       ✅         |


# Examples
## Running CLI on a private VPC instance
Test locally using the following ssh tunnel configuration  
```shell
ssh -D 8080 -C -N  user@example.com
```

## Setting up a new CLI session
Create a client with proxy config session  
```python
from mwaacli.mwaa import MWAACLI
cli = MWAACLI(
    'example-mwaa-environment',
    boto3.client('mwaa'),
    proxies={'https': 'socks5://0:8080'}
)
```
Create a client passing in your own session  
```python
from mwaacli.mwaa import MWAACLI
cli = MWAACLI(
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
date = datetime.now()
run = DAGRun()._from_openapi_data(
    dag_id=dag_id,
    execution_date=date,
    dag_run_id="dag_run_id_example"+date.__str__(),
    conf={'key': 'val'},
)
cli.new_dagrun(run)
```
