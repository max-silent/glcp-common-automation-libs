# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath("../../automation_libs"))
print(sys.path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "CAFE Shared Libraries"
copyright = "(C) Copyright 2023 Hewlett Packard Enterprise Development LP"
author = "HPE Engineering Authors"
release = "1.0.0"
today_fmt = "%Y-%m-%d %H:%M:%S UTC"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
# napoleon_google_docstring = False

templates_path = ["_templates"]
exclude_patterns = []
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://stackoverflow.com/questions/32858931/how-to-stop-sphinx-automethod-prefixing-method-name-with-class-name
add_module_names = False

html_theme = "bizstyle"
html_theme_options = {
    "sidebarwidth": 450,
    "rightsidebar": "true",
}

html_static_path = ["_static"]
