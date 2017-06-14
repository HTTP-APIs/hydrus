Hydrus
===================
Hydrus is a set of **Python** based tools for easier and efficient creation of Hypermedia driven REST-APIs. Hydrus utilises the power of [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to create a powerful REST APIs to serve data.
Hydrus uses the [Hydra(W3C)](http://www.hydra-cg.com/) standard for creation and documentation of it's APIs.

Table of contents
-------------
* [Features](#features)
* [Requirements](#req)
* [Usage](#usage)
    * [Setting up the database](#dbsetup)
    * [Adding data](#adddata)
    * [Setting up the server](#servsetup)
    * [Testing the server](#testserv)
    * [Using the client](#useclient)
* [Design](#design)
    * [Database Design](#dbdesign)
    * [Use cases](#usecase)

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

Apart from this, there are also various Python packages that Hydrus uses. A list of all these packages can be found in the [requirements](requirements.txt) file. It would be advisable to run **`pip install -r requirements.txt`** before setting up other things.

<a name="usage"></a>
Usage
-------------
This section explains the basic usage and setup of Hydrus.


<a name="design"></a>
Design
-------------
The design of the Database takes into account the different types of representations possible using the triple format.
Typically, there are 4 types of triples that are stored in a `Graph`:
- `Class >> Property >> Class` [GraphCAC]
- `Resource >> Property >> Class` [GraphIAC]
- `Resource >> Property >> Resource` [GraphIII]
- `Resource >> Property >> Value` [GraphIIT]

For a distinction between the different types of `Value`, we created a `Terminal` class, which contains a `value` and it's `unit`.
There is also a distinction between properties that map to `Resources` and `Terminals` and those that map to `Classes`.
We call `Properties` that map to `Classes` as `AbstractProperty` and the other as `InstanceProperty`.

Below is the schema diagram for our database design:

![DB Schema](docs/wiki/images/db_schema.svg?raw=true "Schema")


<a name="design"></a>
This section explains Hydrus's design and a use case for the same.
For the demonstration, the server has the [Subsystems](http://ontology.projectchronos.eu/documentation/subsystems) and [Spacecraft](http://ontology.projectchronos.eu/documentation/spacecraft) vocabularies.

Here is an example of a system used to serve data using the components of Hydrus:

![Use case](docs/wiki/images/use_case1.png?raw=true "Use case")

#### A simple example explaining the use of the above architecture would be:
* User types in the query “What is the cost of a Thermal Subsystem?”.
* Middleware uses NLP to extract keywords `Thermal Subsystem` and `cost` and maps it to the Hydra instances and properties present at the server.
* Middleware passes these instances and the underlying query to the client.
* Client models a request and uses the API endpoints to extract the given information from the server.
* Server replies with the required value.
* Client serves data to the User.
