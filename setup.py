from setuptools import find_packages, setup

setup(
    name='mwaacli',
    version='0.1.0',
    author='Gregory Wiltshire',
    author_email='mellon.greg@gmail.com',
    packages=find_packages(exclude=['tests']),  # Include all the python modules except `tests`.
    description='Python Client for Apache CLI on AWS Managed Airflow',
)
