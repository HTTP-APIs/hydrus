hydrus [![Build Status](https://travis-ci.com/HTTP-APIs/hydrus.svg?branch=master)](https://travis-ci.com/HTTP-APIs/hydrus)
===================
hydrus is a set of **Python** based tools for easier and efficient creation of Hypermedia driven REST-APIs. hydrus utilises the power of [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to create a powerful REST APIs to serve data.
hydrus uses the [Hydra(W3C)](http://www.hydra-cg.com/) standard for creation and documentation of it's APIs.

Table of contents
-------------
* [Features](#features)
* [Requirements](#req)
* [Demo](#demo)
* [Usage](#usage)

<a name="features"></a>
Features
-------------
hydrus supports the following features:
- A client that can understand Hydra vocabulary and interacts with a Hydra supporting server to basic [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on data.
- A generic server that can serve required data and metadata(in the form of API documentation) to a client over HTTP.
- A middleware that allows users to use the client to interact with the server using Natural Language which is processed machine consumable language. **(under development)**

<a name="req"></a>
Requirements
-------------
The system is built over the following standards and tools:
- [Flask](http://flask.pocoo.org/) a Python based micro-framework for handling server requests and responses.
- [JSON-LD](http://json-ld.org/spec/latest/json-ld/) as the preferred data format.
- [Hydra](http://www.hydra-cg.com/) as the API standard.
- [SQLAlchemy](http://www.sqlalchemy.org/) as the backend database connector for storage and related operations.

Apart from this, there are also various Python packages that hydrus uses. Using `python setup.py install` installs all the required dependencies.

**NOTE:** You'll need to use `python3` not `python2`.

<a name="demo"></a>
Demo
-------------
To run a demo for hydrus using the sample API, just do the following:

Clone hydrus:
```bash
git clone https://github.com/HTTP-APIs/hydrus
```
Change directory and switch to the develop branch:
```bash
cd hydrus

git checkout -b develop origin/develop
```

Install hydrus using:
```bash
pip install .
```
or
```bash
python setup.py install
```

and run the server using:

```bash
hydrus serve
```

The demo should be up and running on `http://localhost:8080/serverapi/`.

<a name="usage"></a>
Usage
-------------
For more info, head to the [Usage](http://www.hydraecosystem.org/01-Usage.html) section of the [wiki](http://www.hydraecosystem.org/).
