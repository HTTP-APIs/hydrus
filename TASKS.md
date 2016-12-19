
Establish a protocol for building routes in a way that can fit the HYDRA spec:

* Every route (see `server.routes.py`) has to be documented with a `hydra:ApiDocumentation` (automatically): it can be used the Werkzeug `Rule.endpoints` property to name each route (within the `add_url_rule` method) and map to an apidoc response;
* Rejoin all the different vocabularies in just one big vocabulary and make the server filter by argument if necessary (example vocabulary are "astronomy" and "solarsystem");
* Routes, outside the basic collections, has to be opinionated considering the concern of filtering and data creation required by the instantiation of the objects based on the provided classes (*or do it in a separate layer above*); in this case we would have a "smart middleware" that relies on a lower server layer. 
* Start with the lower layer, that should be meant to provide resource one-by-one or by collections