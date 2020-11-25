#!/usr/bin/env python
"""Setup script for Hydrus."""

from setuptools import setup, find_packages

setup(
    name="hydrus",
    include_package_data=True,
    version="0.3.1",
    description="Hydra Ecosystem Flagship Server. Deploy REST data for Web 3.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Hydra Ecosystem",
    author_email="collective@hydraecosystem.org",
    url="https://github.com/HTTP-APIs/hydrus",
    py_modules=["cli"],
    python_requires=">=3.5.2",
    packages=find_packages(exclude=["contrib", "docs", "tests*", "hydrus.egg-info"]),
    package_dir={"hydrus": "hydrus"},
    entry_points="""
            [console_scripts]
            hydrus=cli:startserver
        """,
)
