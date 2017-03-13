from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

NAME = 'smartsheet-python-sdk'

REQUIRES = [
    'requests',
    'requests-toolbelt',
    'six >= 1.9',
    'certifi',
    'python-dateutil'
]
# test packages:
# https://github.com/coagulant/coveralls-python
# https://github.com/pytest-dev/pytest

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name=NAME,
    description='Library that uses Python to connect to Smartsheet services (using API 2.0).',
    author='Smartsheet',
    author_email='api@smartsheet.com',
    url='http://smartsheet-platform.github.io/api-docs/',
    license='Apache-2.0',
    keywords=['Smartsheet', 'Collaboration', 'Project Management', 'Excel', 'spreadsheet'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
    use_scm_version={
        'write_to': 'smartsheet/version.py'
    },
    setup_requires=['setuptools_scm'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.rst').read(),
    extras_require={
        'test': ['coverage', 'coveralls', 'pytest'],
        'develop': [
            'coverage',
            'coveralls[yaml]',
            'pytest',
            'pytest-instafail'
        ]
    },
    tests_require=['pytest'],
    cmdclass={
        'test': PyTest
    }
)
