#!/bin/sh

set -ev

git clone https://github.com/smartsheet-platform/smartsheet-sdk-tests.git
smartsheet-sdk-tests/travis_scripts/install_wiremock.sh

pip install --upgrade pip
pip install certifi
pip install enum34 requests six python-dateutil coverage coveralls[yaml] pytest pytest-travis-fold pytest-instafail requests-toolbelt

smartsheet-sdk-tests/travis_scripts/start_wiremock.sh
coverage run --source=smartsheet setup.py test -a tests/integration/

coveralls --verbose
