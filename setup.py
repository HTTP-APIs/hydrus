# !/usr/bin/env python
"""Setup script for Hydrus."""

from distutils.core import setup

setup(name='hydrus',
      version='0.0.1',
      description='A space-based application for W3C HYDRA Draft',
      author='W3C HYDRA development group',
      author_email='public-hydra@w3.org',
      url='https://github.com/HTTP-APIs/hydrus',
      install_requires=[
          'Flask==0.11',
          'Flask-RESTful==0.3.6',
          'gevent==1.2.2',
          'greenlet==0.4.12',
          'Jinja2==2.9.6',
          'MarkupSafe==1.0',
          'SQLAlchemy==1.1.10',
          'Werkzeug==0.12.2',
          'aniso8601==1.2.1',
          'appdirs==1.4.3',
          'argparse==1.2.1',
          'click==6.7',
          'itsdangerous==0.24',
          'lifter==0.4.1',
          'packaging==16.8',
          'persisting-theory==0.2.1',
          'psycopg2',
          'pyparsing==2.2.0',
          'python-dateutil==2.6.0',
          'pytz==2017.2',
          'six==1.10.0',
          'thespian==3.5.2',
          'flask-cors',
          'blinker==1.4',
      ],
      packages=[
        'hydrus',
      ],
      package_dir={'hydrus':
                   'hydrus'},
      )
