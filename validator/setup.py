#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

setup(
    name='validator',
    version='0.1.0',
    author='Anthony Miyaguchi',
    author_email='amiyaguchi@mozilla.com',
    description='Spark schema validation job',
    url='https://github.com/acmiyaguchi/schema-validator',
    install_requires=[
        "pyspark",
        "click",
        "jsonschema",
    ],
    packages=['validator'],
    package_dir={'validator': 'validator'},
)
