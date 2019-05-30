hydrus [![Build Status](https://travis-ci.com/HTTP-APIs/hydrus.svg?branch=master)](https://travis-ci.com/HTTP-APIs/hydrus)
===================
hydrus is a set of **Python** based tools for easier and efficient creation of Hypermedia driven REST-APIs. hydrus utilises the power of [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to create a powerful REST APIs to serve data.
hydrus uses the [Hydra(W3C)](http://www.hydra-cg.com/) standard for creation and documentation of it's APIs.

Start-up the demo
-----------------
* with *Docker* and *docker-compose* installed, run `docker-compose up --build`
* open the browser at `http://localhost:8000/api/vocab`

You should be displaying the example API as served by the server.

Add your own Hydra documentation file
-------------------------------------
To serve your own Hydra-RDF documentation file:
* create a `doc.py` file as the ones in `examples/` directory containing your own *ApiDoc*
* set the `APIDOC_REL_PATH` variable in `docker-compose.yml`. This should the relative path from the project root
* start-up the demo as above.

You should be displaying your API as served by the server.

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
pip3 install -r requirements.txt

python3 setup.py install
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
=======
hydrus [![Build Status](https://travis-ci.com/HTTP-APIs/hydrus.svg?branch=master)](https://travis-ci.com/HTTP-APIs/hydrus)
===================
hydrus is a set of **Python**-based tools for easier and more efficient creation of Hypermedia driven REST-APIs. hydrus utilises the power of [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to create powerful REST APIs to serve data.
hydrus uses the [Hydra(W3C)](http://www.hydra-cg.com/) standard for creation and documentation of its APIs.

Start-up the demo
-----------------

#### Automatic with Docker:
* with *Docker* and *docker-compose* installed, run `docker-compose up --build`
* open the browser at `http://localhost:8000/api/vocab`

You should be displaying the example API as served by the server.

#### Manually:
You can install the library in your project from latest Github release with `pip install git+git://github.com/http-apis/hydrus.git#egg=hydrus`; or from PyPi with: `pip install hydrus`.  

Add your own Hydra documentation file
-------------------------------------
To serve your own Hydra-RDF documentation file:
* create a `doc.py` file as the ones in `examples/` directory containing your own *ApiDoc*
* set the `APIDOC_REL_PATH` variable in `docker-compose.yml`. This should the relative path from the project root
* start-up the demo as above.

You should be displaying your API as served by the server.

Table of Contents
=======
* [Features](#features)
* [Requirements](#req)
* [Demo](#demo)
* [Usage](#usage)

<a name="features"></a>
Features
-------------
hydrus supports the following features:
- Be a REST server that understands Hydra vocabulary and performs basic [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on data in a Hydra supporting server. 
- Be a generic server that provides the required data and metadata (in the form of API documentation) to a client over HTTP.

<a name="req"></a>
Requirements
-------------
The system is built over the following standards and tools:
- [Flask](http://flask.pocoo.org/), a Python-based micro-framework for handling server requests and responses.
- [JSON-LD](http://json-ld.org/spec/latest/json-ld/) as the preferred data format.
- [Hydra](http://www.hydra-cg.com/) as the API standard.
- [SQLAlchemy](http://www.sqlalchemy.org/) as the backend database connector for storage and related operations.

Other than this, there are also various Python packages that hydrus uses. Running `python setup.py install` installs all the required dependencies.

**NOTE:** `python3` should be used, not `python2`.

<a name="demo"></a>
Demo
-------------
To run a demo for hydrus using the sample API, do the following:

Clone hydrus:
```bash
git clone https://github.com/HTTP-APIs/hydrus
```
Change directory and switch to the develop branch:
```bash
cd hydrus

git checkout -b develop origin/develop
```

Install hydrus:
```bash
pip install .
```
or
```bash
python setup.py install
```

and run the server:

```bash
hydrus serve
```

The demo should now be running on `http://localhost:8080/serverapi/`.

<a name="usage"></a>
Usage
-------------
For more info, head to the [Usage](http://www.hydraecosystem.org/01-Usage.html) section of the [wiki](http://www.hydraecosystem.org/).

