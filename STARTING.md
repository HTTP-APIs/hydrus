### State of the document
This document is just a collection of annotations at the moment.

### Objectives
This project in basically aimed to solve these issues:
* provide an attractive demo API to show HYDRA specs, we  decided to leverage space sciences as they provide a subject of great interest;
* define a multi-layered (and multi-peer?) approach to make the API usable and adaptable to different filtering/querying needs;
* make useful experiments about the right way to approach aggregation/filtering procedures among data served by multiple HYDRA-enhanced endpoints (starting from well-know industry standards for database management and data warehousing, and some glimpses to GraphQL). 


### Starting assumptions

We suppose the server has to be build with at least two layers of abstraction: a low-level strict-HYDRA-RDF API that can map as directly as possible the data to resources/collections ("Server"), and a middleware API ("Client") to perform some sort of opinionated intermediation between the lower level and the "final" client ("UI") above. The middleware has to implement data querying on the lower endpoints, leveraging HYDRA's metadata framework; to do this it has in some way to implement precise choices about the aggregation mechanism that is going to fetch and "map-reduce" (aggregate) the data from the lower level (this part is really open for discussions, as a starting example you can check Mongo's pipelines and its matching/grouping system); because of the different patterns that makes possible this kind of results, some choices about tools and techniques have to be discussed and options defined. 

### About the option of having endpoints that are type- (class-) based
As we discussed, the fun idea would be to have somenthing that can "mix" REST and RPC in some way, not technically but at least conceptually. This approach comes from the observation that the statefulness of a REST API can be in some sort (at a level we are trying to understand for the purpose of our implementation) related to the concept of invariability of the output of a pure-function. This would be practically accomplished by dedicating some endpoints to resources obviously but also to "operations" (functions that accepts some kind of paramethers and run some kind of reasoning on a data structure, we temporarly define these endpoints `hydra:Operation`s).

### Different layers of API: a simple use-case
What we mean with "aggregation" and "filtering" with HYDRA? Let's see a simple example.

As HYDRA is meant to let clients to interoperate automatically, we try here to subset the problem posing it on this shape: starting from an initial input from a human/user, how can different layers of HYDRA-featured APIs respond consistantly by querying the provided endpoints? 
* "UI" layer: a user (or a machine from another network) is wishful to know "what is most distant from the Sun, Earth or Mars?"
* "Client" layer: the client knows that some endpoints are available at a lower level, and we suppose that it knows it has to look for some kind of length value. It looks for the endpoints that can help, we suppose it can understand the fact that it needs the `/api/planet/calculate_average_au` (look for the right operation to perform on the "planet" class, that is basically a documentation problem); so it pass the parameters (Earth and Mars) to it. This layer is commonly referred to as *middleware*; we temporarly define `/api/planet/calculate_average_au` as a `hydra:Operation` (an endpoint that performs come kind of aggregation on other endpoints, something more similar to an RPC call more than a REST call probably), all the `hydra:Operation`s referred to a `hydra:Class` type has to be listed in the class' definition; 
* "Server" layer: the server endpoints are queried and they serve the required data to calculate and respond: "Mars!". This server is the one that works like a traditional HYDRA-enhanced API, with all the descriptive features provided by the spec. 

In this scenario, allowed operations are defined by the possible interaction of different (or same-kind) classes (this idea is inspired by the Scala programming language's typing system). For example, two instances of a `Planet` (of the Solar System) class can have in common the defined "operation" of `calculate_average_au` (compute the average distance of two planets using the Sun-Earth distance as unit(AU)). This way in the API we could do: `/api/planet/calculate_average_au` and pass to it the related parameters.

This kind and body of the request:
```
POST /api/planet/calculate_average_au
{
   @type: "hydra:Collection",
   "hydra:member": [
       {"@id": "/api/planet/earth", "@type": "astronomy:Planet"}, 
       {"@id": "/api/planet/mars", "@type": "astronomy:Planet"},
   ]
}
```
This endpoint could respond with:
```
{
   @type: "vocab:Result",  # or the given type in the HYDRA framework
   @returns: "umbel:Float",
   "unit": "dbpedia:Astronomical_unit"
   "value": "0.523"
}
```
This RPC-like endpoint could be meta-described as:
```
{
    "@context": {
      "hydra": "http://www.w3.org/ns/hydra/context.jsonld"
    },
    "@id": "/api/hydra/planet/calculate_average_au".format(view),
    @type: ["hydra:Operation", "hydra:ApiDocumentation"],
    "hydra:title": "Calculate distance in AU",
    "hydra:description": "...",
    "hydra:entrypoint": "/api/planet/calculate_average_au",
    "hydra:supportedClass": [
      
    ],
    "hydra:possibleStatus": [

    ],
    "result_type": "dbpedia:Length"  # a taxonomy of measurement units is availble at opencyc.org
    @returns: "umbel: Float"
}
```


### Stack
* initial version: local Flask ("Server") and in-memory low-footprint actors ("Client") reading from local vocabularies, use ZeroMQ;
* development version: use a cache (Mongo or Redis) for documents and try to represent a graph;
* stable version: add a some kind of graph database under the cache layer;
* ...

### Implementation

#### Starting idea
* Let Flask("Server") and the Actor System("Client") to communicate via ZeroMQ. Major concern: how to make the worker to be run into a Request (maybe implementing Celery could be easier in the beginning).

