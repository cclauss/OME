# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Open Metadata Exchange"
version = "0.0.1"
copyright = "2024, ISKME and contributors"
author = "ISKME and contributors"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    "_build",
    ".DS_Store",
    "requirements.txt",
    "Thumbs.db",
]
extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
]
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_fence_as_directive = [
    "mermaid",
]
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
    ".txt": "markdown",
}
suppress_warnings = ["epub.unknown_project_files"]
templates_path = ["_templates"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]
html_theme = "alabaster"
