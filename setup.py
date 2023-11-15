"""Setup file for the Sphinx doc."""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
# README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="hpe_glcp_automation_libs",
    version="1.0.0",
    description="CAFE Shared Libraries",
    long_description="Documentation for the CAFE shared libraries.",
    long_description_content_type="text/x-rst",
    url="https://github.com/glcp/glcp-common-automation-libs",
    author="HPE Engineering Authors",
    author_email="vui.le@hpe.com",
    license="HPE proprietary",
    classifiers=[
        "License :: HPE proprietary",
        "Programming Language :: Python",
    ],
    keywords="sphinx",
    packages=setuptools.find_packages(),
    # entry_points={"console_scripts": ["tree-cli=trees.bin.tree_cli:main"]},
    python_requires=">=3.10",
)
