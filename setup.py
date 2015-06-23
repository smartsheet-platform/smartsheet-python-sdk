from setuptools import setup

setup(
        name='smartsheetclient',
        version='0.0.1',
        author='Scott Wimer',
        author_email='scott.wimer@smartsheet.com',
        description='Client for interacting with the Smartsheet API',
        license='Copyright Smartsheet, Inc. 2014, all rights reserved',
        packages=[
            'smartsheetclient',
            'smartsheetclient.client_1_1',
        ],
        package_dir={
            'smartsheetclient': 'src/python/smartsheetclient',
            'smartsheetclient.client_1_1':
                'src/python/smartsheetclient/client_1_1',
        },
        install_requires=['httplib2']
)
