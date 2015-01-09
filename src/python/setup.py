import os
from setuptools import setup, find_packages

setup(
        name='smartsheetclient',
        version='0.0.1',
        author='Scott Wimer',
        author_email='scott.wimer@smartsheet.com',
        description='Client for interacting with the Smartsheet API',
        license='Copyright Smartsheet, Inc. 2014, all rights reserved',
        packages=find_packages('.'),
        install_requires=['httplib2']
    )

