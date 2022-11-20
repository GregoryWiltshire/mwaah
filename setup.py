from setuptools import find_packages, setup

setup(
    name='mwaacli',
    version='0.1.0',
    requires=[
        'git+https://github.com/apache/airflow-client-python@2.2.0#egg=apache-airflow-client',
        'botocore>=1.20.0',
        'boto3',
        'requests',
        'pydantic',
    ],
    extras_require={
        'socks': ['PySocks>=1.5.6, !=1.5.7'],
    },
    author='Gregory Wiltshire',
    author_email='mellon.greg@gmail.com',
    packages=find_packages(exclude=['tests']),  # Include all the python modules except `tests`.
    url='https://github.com/GregoryWiltshire/mwaacli-python',
    description='Python Client for Apache CLI on AWS Managed Airflow',
)
