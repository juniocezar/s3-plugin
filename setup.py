#!/usr/bin/env python
import sys
from setuptools import setup

requires = ['awscli>=1.11.0']

setup(
    name='sidecar-awscli-s3-plugin',
    packages=['sidecar-awscli-s3-plugin'],
    version='0.1',
    description='S3 proxy plugin for AWS CLI',
    long_description=open('README.md').read(),
    author='Sebastian Nowak | Updated by Junio Cezar',
    author_email='',
    url='',
    download_url='',
    keywords=['awscli', 'plugin', 's3', 'proxy'],
    install_requires=requires,
    classifiers = []
)
