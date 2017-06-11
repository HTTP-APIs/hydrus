#!/usr/bin/env python

from distutils.core import setup

setup(name='hydrus',
      version='0.0.1',
      description='A space-based application for W3C HYDRA Draft',
      author='W3C HYDRA development group',
      author_email='public-hydraspec@w3.org',
      url='https://github.com/HTTP-APIs/hydrus',
      install_requires=['flask==0.11', 'thespian==3.5.2', 'lifter==0.4.1'],
      packages=[
        'hydrus',
      ],
      package_dir={'hydrus':
                    'hydrus'},
)
