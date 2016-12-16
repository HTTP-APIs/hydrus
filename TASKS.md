
Establish a protocol for building routes in a way that can fit the HYDRA spec:

* Every route (see `server.routes`) has to be documented with a `hydra:apiDocumentation` (automatically): it can be used the Rule.endpoints property to name each route (with the `add_url_rule` method) and map to an apidoc response;
* Rejoin all the different vocabularies in just one big vocabulary and make the server filter by argument if necessary;
* Routes, outside the basic collections, has to be opinionated considering the concern of filtering and data creation required by the instantiation of the objects based on the provided classes; 