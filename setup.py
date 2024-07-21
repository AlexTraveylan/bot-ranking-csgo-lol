"""
This file is the setup script for the package.
"""

from setuptools import find_packages, setup

setup(
    name="<app_name>",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy", "pandas", "PyArrow"],
)
