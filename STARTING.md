### About the option of having endpoints that are type- (class-) based
As we discussed, the fun idea would be to have somenthing that can "mix" REST and RPC in some way, not technically but at least conceptually. This approach comes from the observation that the statefulness of a REST API can be in some sort (at a level we are trying to understand for the purpose of our implementation) related to the concept of invariability of the output of a pure-function. This would be practically accomplished by dedicating some endpoints to resources obviously but also to "operations" (functions that accepts some kind of paramethers and run some kind of reasoning on a data structure).

In this scenario, allowed operations are defined by the possible interaction of different (or same-kind) classes. For example, two instances of a `Planet` (of the Solar System) can have in common the defined "operation" of `calculate_average_au` (compute the average distance of two planets using the Sun-Earth distance as unit(AU)). This way in the API we could do: `/api/planet/calculate_average_au` and pass to it the related parameters.

This kind and body or the request:
```
POST /api/planet/calculate_average_au
{
   @type: "hydra:Collection",
   parameters: [
       "earth", "mars"
   ]
}
```
This endpoint could respond with:
```
{
   @type: "vocab:Result",  # or the given type in the HYDRA framework
   @returns: "umbel:Float",
   unit: "dbpedia:Astronomical_unit"
   value: "0.523"
}
```
This endpoint would be meta-described as:
```
{
   @type: "hydra:Operation",
   ...
}
```


### Different layers of API
