"""
Experimenting the possibility to use a local Actor mini-System to
let each request to creates a local representation of the needed 
resources and retrieve the needed data.

Actors will retrieve data via requests or local storage or cache.

Example use case: 
* application needs the radius of planet Mars and send a request to 
  the dedicated endpoint;
* the handler asks the actor system. An actor of type "PlanetTypeActor" with
  "name" equals "Mars" is spawned and the same for its closests nodes; 
* The actor takes the value of the "sameAs" property and looks in the cache
  or sends a request to DBpedia.org; if succeed it sends the response body to
  a parser actor;
* the parser actor find the value of the radius in the response and send it
  back to the resource actor;
* the resource actor (the instance of "PlanetTypeActor") routes the datum back
  to the response and its lifecycle ends;
* the handler responds.
"""
from thespian.actors import Actor
from hydrus.server.application import system


# a classes factory that creates actor types based on the @type


#+-------------------------+             +---------------------------------+
#|                         |             |                                 |
#|  JSON-LD structure      |             | Actor Types Factory             |
#|                         |             |                                 |
#|  {                      |             |    SomeResourceTypeActor        |
#|    @context: "Some",    |     loads   |    SomeOtherTypeActor           |
#|    "defines": [         | <-----------+    ...                          |
#|       {}, {}, {}, {}    | |           |                                 |
#|    ]                    | | i         |                                 |
#|  }                      | | n         |                                 |
#|                         | | s         |                                 |
#+-------------------------+ | t         +---------------------------------+
#                            | a
#                            | n
#                            | c
#                            v e
#           l |         +------+-e-----------+
#           o |         | Actor              |
#           c |         |                    |   owl#isSubClassOf
#           a |         | SomeResource       +--------------------+
#           l |         | @type: owl#Class   |                    |
#             |         | sameAs: http://..  |                    |
#           m |         +--------------------+                    |
#           i |                                                   |
#           n |                 +----------------------+          |
#           i |                 | Actor                |          |
#           - |                 |                      |          |
#           s |                 | SomeOtherType        +----------+
#           y |                 | @type: owl#Class     |
#           s |                 | sameAs: http://..    | 
#           t |                 +----------------------+
#           e |
#           m |