Hydrus
===================
Hydrus is a set of **Python** based tools for easier and efficient creation of Hypermedia driven REST-APIs. Hydrus utilises the power of [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to create a powerful REST APIs to serve data.
Hydrus uses the [Hydra(W3C)](http://www.hydra-cg.com/) standard for creation and documentation of it's APIs.

Table of contents
-------------
* [Features](#features)
* [Requirements](#req)
* [Demo](#demo)
* [Usage](#usage)
* [Design](#design)

<a name="features"></a>
Features
-------------
Hydrus supports the following features:
- A client that can understand Hydra vocabulary and interacts with a Hydra supporting server to basic [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on data.
- A generic server that can serve required data and metadata(in the form of API documentation) to a client over HTTP.
- A middleware that allows users to use the client to interact with the server using Natural Language which is processed machine consumable language. **(under developement)**

<a name="req"></a>
Requirements
-------------
The system is built over the following standards and tools:
- [Flask](http://flask.pocoo.org/) a Python based micro-framework for handling server requests and responses.
- [JSON-LD](http://json-ld.org/spec/latest/json-ld/) as the prefered data format.
- [Hydra](http://www.hydra-cg.com/) as the API standard.
- [PostgreSQL](https://www.postgresql.org/) as the backend database for storage and CRUD operations.

Apart from this, there are also various Python packages that Hydrus uses. A list of all these packages can be found in the [requirements.txt](https://github.com/HTTP-APIs/hydrus/blob/master/requirements.txt) file. It would be advisable to run **`pip install -r requirements.txt`** before setting up other things.

<a name="demo"></a>
Demo
-------------
**Please make sure you have [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/) installed.**

Once we have docker up and running setting up the demo server is a piece of cake.
### Running the demo server
- Clone the repository to your local machine.
- `cd` into the project directory and use `docker-compose build` to build the required docker containers.
- Start the containers using `docker-compose up`(With this we have our demo server up and running).
- Now, all we need to do is setup and populate the database. Connect to the container using <br/> `docker exec -i -t <container_name or container_id> /bin/bash` ( You can get the hydrus container name using `docker ps`. It should be something like `hydrus*`).
- Create the database models using `python /app/hydrus/data/db_models.py`.
- Parse and insert classes from RDF/OWL vocabulary to the database using `python /app/hydrus/data/insert_classes.py`
- Insert random data generated  by `hydrus.data.generator` using `python /app/hydrus/data/insert_data.py`. <br/>
**NOTE**: This step is only valid for the subsystem example. You'll need to write your own generator to populate the database for any other example.
- Exit the docker container shell using `exit`.

**The demo server should be up and running at `127.0.0.1:8080/api`.**

**NOTE:** Docker port binding is not working in Windows. Windows users can access the server at `<docker_ip>:8080/api`. You can check your docker_ip using `docker-machine ip`.


<a name="usage"></a>
Usage
-------------
To understand how to use Hydrus and how things work, head over to the [Usage](Usage) page of the wiki.

<a name="design"></a>
Design
-------------
Head over to the [Design](Design) page to understand the design principles and use cases of Hydrus.
