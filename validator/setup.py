#!/usr/bin/env python
# encoding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

setup(
    name='mozschema-validator',
    version='0.0.1',
    author='Anthony Miyaguchi',
    author_email='amiyaguchi@mozilla.com',
    description='Spark schema validation job',
    url='https://github.com/acmiyaguchi/mozschema-validator',
    packages=['mozvalidator'],
    package_dir={'mozvalidator': 'mozvalidator'},
)
