#!/bin/sh

make_docs() {
  rm -f docs-source/smartsheet.rst
  rm -f docs-source/smartsheet.models.rst
  rm -f docs-source/modules.rst
  sphinx-apidoc -o docs-source smartsheet
  rm -rf docs-source/_build
  sphinx-build -b html -d docs-source/_build/doctrees docs-source/. docs-source/_build/html
  rm -rf docs
  cp -a docs-source/_build/html docs/
  cp .nojekyll docs
}

install_packages() {
  pip install enum34 requests six python-dateutil
  pip install sphinx
  pip install sphinx_rtd_theme
  pip install setuptools-scm
  pip install gitchangelog mako
  pip install collective.checkdocs
  pip install twine
}

set -e
export RELEASE_TAG=${deploy}
install_packages
echo "beginning deploy..."

# git configuration
git config --global user.email "travis@travis-ci.org"
git config --global user.name "Automated Build"

echo "docs 1st pass..."
make_docs
git add docs/*
git commit -am "chg: doc: build ${RELEASE_TAG} docs 1st pass"
git push https://${GH_USER}:${GH_ACCESS_TOKEN}@github.com/smartsheet-platform/smartsheet-python-sdk.git \
    HEAD:${TRAVIS_BRANCH} > /dev/null 2>&1

echo "updating release tag..."
git tag ${RELEASE_TAG} -m "Release ${RELEASE_TAG}"
git push https://${GH_USER}:${GH_ACCESS_TOKEN}@github.com/smartsheet-platform/smartsheet-python-sdk.git HEAD:${TRAVIS_BRANCH} --tags > /dev/null 2>&1

echo "building distribution..."
# note this must be done immediately after the tag and before other files are committed
# to avoid setuptools_scm from designating the distribution with an interim dev tag.
python setup.py checkdocs
python setup.py sdist bdist_wheel
echo "uploading distribution..."
twine upload -u "smartsheet-platform" -p ${PYPI_PASSWORD} dist/*

echo "docs final pass..."
make_docs
git add docs/*
git commit -am "chg: doc: build ${RELEASE_TAG} final docs"
git push https://${GH_USER}:${GH_ACCESS_TOKEN}@github.com/smartsheet-platform/smartsheet-python-sdk.git \
    HEAD:${TRAVIS_BRANCH} > /dev/null 2>&1
echo "update CHANGELOG.md..."

gitchangelog
git add CHANGELOG.md
git commit -am "chg: doc: update CHANGELOG.md"
git push https://${GH_USER}:${GH_ACCESS_TOKEN}@github.com/smartsheet-platform/smartsheet-python-sdk.git \
    HEAD:${TRAVIS_BRANCH} > /dev/null 2>&1
