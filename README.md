# Hydrus

DISCLAIMER: this repo is only a collection of annotations at the moment, don't take them too seriously.

A project to develop a space sciences-based application to demonstrate features provided by [HYDRA](http://www.hydra-cg.com/spec/latest/core)-powered HTTP APIs.

At the moment: start from [STARTING.md](STARTING.md)

### Running
* In the repo directory `python3 hydrus/application.py`

### Testing
* `curl -i localhost:5000/api`
* `curl -i localhost:5000/api/astronomy`
* `curl -i localhost:5000/api/solarsystem`
* `curl -i localhost:5000/api/hydra/astronomy`
* `curl -i localhost:5000/api/hydra/solarsystem`
* `curl -X POST localhost:5000/api/planet/create -d '{"@id": "/api/planet/Mars", "@type": "astronomy:Planet"}'`
