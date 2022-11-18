from setuptools import find_packages, setup
setup(
    name='mwaacli',
    version='0.0.0',
    packages=find_packages(exclude=['tests']),  # Include all the python modules except `tests`.
    description='My custom package tested with tox',
    long_description='A long description of my custom package tested with tox',
    install_requires=[
        # Additional requirements, or parse the requirements file and add it here
    ],
    classifiers=[
        'Programming Language :: Python',
    ],
    # entry_points={
    #     'pytest11': [
    #         'tox_tested_package = tox_tested_package.fixtures'
    #     ]
    # },
)
