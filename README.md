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
        * [Classes and Properties](#classprop)
        * [Instances](#instance)
    * [Manipulating data](#moddata)
        * [CRUD operations](#crud)
        * [Exceptions](#error)
    * [Setting up the server](#servsetup)
    * [Running tests](#test)
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

<a name="dbsetup"></a>
### Setting up the database
The databse models use SQLAlchemy as an ORM Layer mapping relations to Python Classs and Objects. A good reference for the ORM can be found [here](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html)

The `engine` parameter in `hydrus.data.db_models` is used to connect to the database. This needs to be modified according to the type of connection:
For example, if the database is an SQLite database, the engine parameter would be as follows:

```python
from sqlalchemy import create_engine

hydrus.data.db_models.engine = create_engine('sqlite:///path/to/database/file')
```
Once the engine is setup, the creation of the required tables can be done as follows:

```python
from hydrus.data.db_models import Base

Base.metadata.create_all(hydrus.data.db_models.engine)
```
This will successfully create all required models in the specified database.

<a name="adddata"></a>
### Adding data
Now that the database models have been setup, we need to populate them with data.

<a name="classprop"></a>
#### Adding Classes and Properties
The first step in adding data is adding the RDFClasses and Properties that the server must support. There are three ways to do this:

The first is to manually add all RDFClasses and Properties. Here are some examples:
```python
'''Adding a new RDFClass'''
from hydrus.data.db_models import RDFClass, engine
from sqlalchemy.orm import sessionmaker

thermal = RDFClass(name="Subsystem_Thermal")    # Creates a new RDFClass instance

# Add the instance to the database
Session = sessionmaker(bind=models.engine)
session = Session()
session.add(thermal)
session.commit()
session.close()
```
```python
'''Adding a new Property'''
from hydrus.data.db_models import AbstractProperty, InstanceProperty, engine
from sqlalchemy.orm import sessionmaker

subclassof = AbstractProperty(name="SubClassOf")    # Creates a new AbstractProperty instance
cost = InstanceProperty(name="hasMonetaryValue")    # Creates a new InstanceProperty instance

# Add the instance to the database
Session = sessionmaker(bind=models.engine)
session = Session()
session.add(subclassof)
session.add(cost)
session.commit()
session.close()
```
The second way to add RDFClasses and Properties is to provide the Hydra APIDocumentation of the API
```python
import hydrus

data = {
    "@context": "http://www.w3.org/ns/hydra/context.jsonld",
    "@id": "http://api.example.com/doc/",
    "@type": "ApiDocumentation",
    "title": "The name of the API",
    "description": "A short description of the API",
    "entrypoint": "URL of the API's main entry point",
    "supportedClass": [
        # ... Classes known to be supported by the Web API ...
        {
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "@id": "http://api.example.com/doc/#Comment",
            "@type": "Class",
            "title": "The name of the class",
            "description": "A short description of the class.",
            "supportedProperty": [
            # ... Properties known to be supported by the class ...
            ]
        },
    ],
    "possibleStatus": [
        # ... Statuses that should be expected and handled properly ...
    ]
}

classes = hydrus.data.doc_parse.get_classes(data)
properties = hydrus.data.doc_parse.get_all_properties(classes)
hydrus.data.doc_parse.insert_classes(classes)
hydrus.data.doc_parse.insert_properties(classes)
```

The final way to add classes and properties to Hydrus is to use RDF/OWL definitions of the classes. This can be done by using the OWL/RDF parser to create Hydra APIDocumentation and then adding data as explained in the previous step.
```python
from hydrus.hydraspec import parser

data = {
    {
       "@type": [
          {
              "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
          }
       ],
       "@id": "http://api.example.com/doc/#Property",
       "rdf:label": "Propertyname"
    },
    {
       "@type": "http://www.w3.org/2002/07/owl#Class",
       "@id": "http://api.example.com/doc/#Class",
       "rdf:comment": "comment about the class",
       "rdf:label": "Classname",
       "rdfs:subClassOf": [
            # ...List of known class restrictions...
       ],
    }
}

owl_props = parser.get_all_properties(data)     # Get all Owl:Properties

hydra_props = parser.hydrafy_properties(owl_props)      # Convert them to Hydra:Property along with class metadata

owl_classes = parser.get_all_classes(subsystem_data)    # Get all the owl:Classes

hydra_classes = parser.hydrafy_classes(owl_classes, hydra_props)    # Convert each owl:Class into a Hydra:Class with property data

apidoc = gen_APIDoc(hydra_classes)      # Create API Documentation with the Hydra:supportedClass
```
---
#### Adding Instances/Resources
To add objects to the instances for a given class, we first need to define a standard way of declaring instances.
We have given an example of a subsystem instance below
```python
instance = {
    "name": "12W communication",    # The name of the instance must be in "name"
    "object": {
        # The "object" key contains all the properties and their values for a given instance
        "maxWorkingTemperature": 63,    # InstanceProperty: Value, Value is automatically converted to Terminal Object

        # In case the Value for a property is another Resource, we use the following syntax
        "hasDuplicate":{
            "@id": "subsystem/34"   # The "@id" tag gives the ID of the other instance
        }

        # In case the property is an AbstractProperty, the class name should be given as Value
        "category": "Spacecraft_Communication",     # AbstractProperty: Classname, Classname is automatically mapped to relevant RDFClass
    }
}

```
Once we have defined such an `instance`, we can use the built in CRUD operations of Hydrus to add these instances.
```python
from hydrus.data import crud

crud.insert(object_=instance)   # This will insert 'instance' into Instance and all other information into Graph.

# Optionally, we can specify the ID of an instance if it is not already used
crud.insert(object_=instance, id_=1)    #This will insert 'instance' with ID = 1  
```

<a name="moddata"></a>
### Manipulating data
We already saw how `insert` work in the previous section, we will now see how the other crud operations work and what are the errors and exceptions for each of them.

<a name="crud"></a>
#### CRUD opertions
Apart from `insert`, the CRUD operations also support `get`, `delete` and `update` opertions. Here are examples for all three:

GET
```python
from hydru.data import crud
import json

instance = crud.get(id_=1)     # Return the Resource/Instance with ID = 1
print(json.dumps(instance, indent=4))
# Output:
# {
#     "name": "12W communication",
#     "object": {
#         "category": "Spacecraft_Communication",
#         "hasMass": 98,
#         "hasMonetaryValue": 6604,
#         "hasPower": -61,
#         "hasVolume": 99,
#         "maxWorkingTemperature": 63,
#         "minWorkingTemperature": -26
#     }
# }
```
DELETE
```python
from hydru.data import crud
import json

output = crud.delete(id_=1)     # Deletes the Resource/Instance with ID = 1
print(json.dumps(output, indent=4))
# Output:
# {
#   204: "Object with ID : 1 successfully deleted!"
# }
```
UPDATE
```python
from hydru.data import crud
import json

new_object = {
    "name": "14W communication",
    "object": {
        "category": "Spacecraft_Communication",
        "hasMass": 8,
        "hasMonetaryValue": 6204,
        "hasPower": -10,
        "hasVolume": 200,
        "maxWorkingTemperature": 63,
        "minWorkingTemperature": -26
    }
}
output = crud.update(id_=1, object_=new_object)     # Updates the Resource/Instance with ID = 1 with new_object
print(json.dumps(output, indent=4))
# Output:
# {
#   204: "Object with ID : 1 successfully updated!"
# }
```
---
<a name="error"></a>
#### Exceptions
The CRUD operations have a number of checks and conditions in place to ensure validity of data. Here are the exceptions that are returned for each of the operations when these conditions are violated.
NOTE: Relevant all responses are returned in JSON format

GET
```python
# A 404 error is returned when an Instance is not found
{
    404: "Instance with ID : 2 NOT FOUND"
}
```

INSERT
```python
# A 400 error is returned when an instance with a given ID already exists
{
    400: "Instance with ID : 1 already exists"
}

# A 401 error is returned when a given AbstractProperty: Classname pair has an invalid/undefined RDFClass
{   
    401: "The class dummyClass is not a valid/defined RDFClass"
}

# A 402 error is returned when a given Property: Value pair has an invalid/undefined Property
{
    402: "The property dummyProp is not a valid/defined Property"
}

# A 403 error is returned when a given InstanceProperty: Instance pair has an invalid/undefined Instance ID
{   
    403: "The instance 2 is not a valid Instance"
}
```

DELETE
```python
# A 404 error is returned when an Instance is not found
{
    404: "Instance with ID : 2 NOT FOUND"
}
```

The `update` operation is a combination of a `delete` and an `insert` operation. All exceptions for both the operation are inherited by update.

<a name="servsetup"></a>
### Setting up the server
The following section explains how the server needs to be setup to be able to serve the data we added in the previous section.

The generic server is implemented using the [Flask](http://flask.pocoo.org/) micro-framework. To get the server up and running, all you need to do is:
```python
from hydrus.app import app

IP = "127.0.0.1"
port_ = 8000
app.run(host=IP, port=port_)

# The server will be running at http://127.0.0.1:8000/
```

<a name="test"></a>
### Running tests
There are a number of tests in place to ensure that Hydrus functions properly.
For running tests related to ensure the validity of the database run

**`python -m unittest hydrus.data.test_db`**

For running client side tests related to the server, run

**`python -m unittest hydrus.test_app`**

<a name="client"></a>
### Using the client
(Under developement) client not yet ready

<a name="design"></a>
Design
-------------
This section explains the design, architecture and the implementation of Hydrus along with a few use cases for the same.
<a name="dbdesign"></a>
### Database Design
The design of the Database takes into account the different types of representations possible using the triple format.
Typically, there are 4 types of triples that are stored in a `Graph`:
* **`Class >> Property >> Class` [`GraphCAC`]**
* **`Resource >> Property >> Class` [`GraphIAC`]**
* **`Resource >> Property >> Resource` [`GraphIII`]**
* **`Resource >> Property >> Value` [`GraphIIT`]**

For a distinction between the different types of `Value`, we created a `Terminal` class, which contains a `value` and it's `unit`.
There is also a distinction between properties that map to `Resources` and `Terminals` and those that map to `Classes`.
We call `Properties` that map to `Classes` as `AbstractProperty` and the other as `InstanceProperty`.

Below is the schema diagram for our database design:

![DB Schema](docs/wiki/images/db_schema.png?raw=true "Schema")


<a name="usecase"></a>
### Use cases
This section explains Hydrus's design and a use case for the same.
For the demonstration, the server has the [Subsystems](http://ontology.projectchronos.eu/documentation/subsystems) and [Spacecraft](http://ontology.projectchronos.eu/documentation/spacecraft) vocabularies.

Here is an example of a system used to serve data using the components of Hydrus:

![Use case](docs/wiki/images/use_case1.png?raw=true "Use case")

**A simple example explaining the use of the above architecture would be:**
* User types in the query “What is the cost of a Thermal Subsystem?”.
* Middleware uses NLP to extract keywords `Thermal Subsystem` and `cost` and maps it to the Hydra instances and properties present at the server.
* Middleware passes these instances and the underlying query to the client.
* Client models a request and uses the API endpoints to extract the given information from the server.
* Server replies with the required value.
* Client serves data to the User.
