del docs\smartsheet.rst
del docs\smartsheet.models.rst
del docs\modules.rst
sphinx-apidoc -o docs/ smartsheet
sphinx-build -b html docs docs/_build