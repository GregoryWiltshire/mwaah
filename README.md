# AWS MWAA (Managed Workflows for Apache Airflow) CLI - Python


# Supported Apache Airflow CLI commands
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

# Setting up a new CLI session
Create a client with proxy config  
```python
from mwaacli.mwaa import MWAACLI
cli = MWAACLI(
    'example-mwaa-environment',
    boto3.client('mwaa'), proxies={'https': 'socks5://0:8080'}
)
```

## Get Version
```python
from mwaacli.mwaa import MWAACLI
cli = MWAACLI(
    'example-mwaa-environment',
    mwaa_client=boto3.client('mwaa', region_name='example-region-1')
)
print(cli.get_version())
```
```
2.2.2
```

## Trigger 
```python
from mwaacli.mwaa import MWAACLI
cli = MWAACLI(
    'example-mwaa-environment',
    mwaa_client=boto3.client('mwaa', region_name='example-region-1')
)
print(cli.get_version())
```
```
2.2.2
```
