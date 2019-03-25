#!/usr/bin/env python
"""Setup script for Hydrus."""

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession


install_requires = parse_requirements('requirements.txt', session=PipSession())
dependencies = [str(package.req) for package in install_requires]

setup(name='hydrus',
      include_package_data=True,
      version='0.2.3',
      description='Hydra Ecosystem Flagship Server. Deploy REST data for Web 3.0',
      author='Hydra Ecosystem',
      author_email='hydraecosystem@googlegroups.com',
      url='https://github.com/HTTP-APIs/hydrus',
      py_modules=['cli'],
      python_requires='>=3.5.2',
      install_requires=dependencies,
      packages=find_packages(
          exclude=['contrib', 'docs', 'tests*', 'hydrus.egg-info']),
      package_dir={'hydrus':
                   'hydrus'},
      entry_points='''
            [console_scripts]
            hydrus=cli:startserver
        '''
      )
