

* Every route (see `server.routes`) has to be documented with a `hydra:apiDocumentation` (automatically): it can be used the Rule.endpoints property to name each route (with the `add_url_rule` method) and map to an apidoc response;
* Rejoin all the different vocabularies in just one big vocabulary and make the server filter by argument if necessary;
* 