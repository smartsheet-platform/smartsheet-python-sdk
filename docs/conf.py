import sys
import os
from setuptools_scm import get_version

# generate docs for the package located in the directory immediately
# above this directory.
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False


source_suffix = '.rst'

master_doc = 'index'

project = u'Smartsheet Python SDK'
copyright = u'Copyright 2017 Smartsheet.com, Inc.'

version = get_version(root="../")
release = get_version(root="../")

exclude_patterns = ['_build']
html_static_path = ['_static']
pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'

html_show_sourcelink = False
html_show_sphinx = False
htmlhelp_basename = 'Smartsheetdoc'
