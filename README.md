# Hydrus

DISCAIMER: this repo is only a collection of absurd annotations at the moment, don't take them too seriously.

A project to develop a space sciences-based application to demonstrate features provided by [HYDRA](http://www.hydra-cg.com/spec/latest/core) -powered HTTP APIs.

At the moment: start from STARTING.md

### Running
* In the repo directory `python3 application.py`

### Testing
* `curl -i localhost:5000/api`
* `curl -i localhost:5000/api/astronomy`
* `curl -X POST localhost:5000/api/CelestialBody/create -H 'Content-Length: 0'`
