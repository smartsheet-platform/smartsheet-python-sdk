from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

NAME = "smartsheet"

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
    name="smartsheet-python-sdk",
    description="Smartsheet API",
    author_email="api@smartsheet.com",
    url="http://smartsheet-platform.github.io/api-docs/",
    keywords=["Smartsheet API"],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""Programmatic access to Smartsheet.""",
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
