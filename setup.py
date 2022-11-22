from setuptools import find_packages, setup

setup(
    name='mwaah',
    version='0.1.0',
    python_requires=">= 3.7",
    install_requires=[
        'apache-airflow-client',
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
    url='https://github.com/GregoryWiltshire/mwaah',
    description='Python Client for Apache CLI on AWS Managed Airflow',
)
