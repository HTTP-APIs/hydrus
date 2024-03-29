#!/usr/bin/env python
"""Setup script for Hydrus."""

from setuptools import setup, find_packages

try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements

    install_requires = parse_requirements("requirements.txt", session=PipSession())
    try:
        dependencies = [str(package.requirement) for package in install_requires]
    except AttributeError:
        dependencies = [str(package.req) for package in install_requires]  # type: ignore
except ImportError:
    raise ImportError("Your pip version is out of date, please run `pip install --upgrade pip setuptools`")

for package_index, _ in enumerate(dependencies):
    if dependencies[package_index].startswith("git+"):
        dependencies[package_index] = dependencies[package_index].split("=")[1]

setup(
    name="hydrus",
    include_package_data=True,
    version="0.5.0",
    description="Hydra Ecosystem Flagship Server. Deploy REST data for Web 3.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Hydra Ecosystem",
    author_email="collective@hydraecosystem.org",
    url="https://github.com/HTTP-APIs/hydrus",
    py_modules=["cli"],
    python_requires=">=3.5.2",
    install_requires=dependencies,
    packages=find_packages(exclude=["contrib", "docs", "tests*", "hydrus.egg-info"]),
    package_dir={"hydrus": "hydrus"},
    entry_points={
        'console_scripts': [
            'hydrus = cli:startserver',
        ],
    },
)
