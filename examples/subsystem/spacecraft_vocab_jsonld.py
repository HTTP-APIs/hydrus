"""Spacecraft vocabulary from http://ontology.projectchronos.eu/spacecraft/?format=jsonld."""

spacecraft_data = {
    "defines": [
        {
            "skos:prefLabel": "Each instance of spacecraft is a transportation device either deployed entirely in outer space, or one whose trajectories leave the atmosphere of the planet it's launched from, in order to orbit the planet or to travel beyond the planet's gravitational field.",
            "rdfs:subClassOf": [
                {
                    "@id": "http://umbel.org/umbel/rc/SystemOfDevices"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isDeployedIn"
                    },
                    "@type": {
                        "@id": "http://www.w3.org/2002/07/owl#Restriction"
                    },
                    "owl:hasValue": {
                        "@id": "http://live.dbpedia.org/ontology/Outer_space.ntriples"
                    }
                }
            ],
            "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft",
            "chronos:relConcept": {
                "@id": "http://hypermedia.projectchronos.eu/data/dbpediadocs/spacecraft"
            },
            "rdf:comment": "In this set of ontologies a spacecraft is described as a system of devices, a vessel made by different subsystems.",
            "rdf:label": "Spacecraft",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "owl:sameAs": "http://umbel.org/umbel/rc/Spacecraft"
        },
        {
            "skos:prefLabel": "subject is a device or a system of devices that is subsystem of a wider system or device",
            "owl:inverseOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/hasSubSystem"
            },
            "@type": [
                {
                    "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf",
            "rdf:label": "isSubsystemOf"
        },
        {
            "skos:prefLabel": "the subject is a member of a wider artifact, that is a set of artifacts",
            "@type": [
                {
                    "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/spacecraft/isComponentOf",
            "rdf:label": "isComponentOf"
        },
        {
            "owl:inverseOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
            },
            "@type": [
                {"@id": "http://www.w3.org/2002/07/owl#ObjectProperty"}
            ],
            "@id": "http://ontology.projectchronos.eu/spacecraft/hasSubSystem",
            "rdf:label": "hasSubSystem"
        },
        {
            "skos:prefLabel": "A device that is deployed into a spacecraft and works outside Earth lower atmosphere",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft",
            "rdf:comment": "A Device is an artifact with a relatively rigid, set shape, designed for a specific use or to perform a specific function",
            "rdf:label": "Subsystem_Spacecraft",
            "rdfs:subClassOf": [
                {
                    "@id": "http://live.dbpedia.org/ontology/Device.ntriples"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": {"@id": "http://www.w3.org/2002/07/owl#Restriction"},
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                    },
                    "@type": {
                        "@id": "http://www.w3.org/2002/07/owl#Restriction"
                    },
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasPower"
                    },
                    "@type": {"@id": "http://www.w3.org/2002/07/owl#Restriction"},
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMass"
                    },
                    "@type": {"@id": "http://www.w3.org/2002/07/owl#Restriction"},
                    "owl:minCardinality": 1
                }
            ],
            "spacecraft:isComponent": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            }
        },
        {
            "skos:prefLabel": "Payload_Spacecraft",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/spacecraft/Payload_Spacecraft",
            "rdf:comment": "The set of devices that the spacecraft carries for scientific purposes, with their supporting (readout) devices.",
            "rdf:label": "Payload_Spacecraft",
            "rdfs:subClassOf": [
                {
                    "@id": "http://umbel.org/umbel/rc/SystemOfDevices"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/embedSensor"
                    },
                    "@type": {"@id": "http://www.w3.org/2002/07/owl#Restriction"},
                    "owl:minCardinality": 1
                }
            ],
            "spacecraft:isComponent": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            }
        },
        {
            "skos:prefLabel": "a subsystem that holds a sensor",
            "@type": [
                {
                    "@id": "http://www.w3.org/2002/07/owl#AsymmetricProperty"
                },
                {
                    "@id": "http://www.w3.org/2002/07/owl#IrreflexiveProperty"
                },
                {
                    "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
                }
            ],
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:comment": "It is a payload",
            "rdf:label": "embedSensor",
            "@id": "http://ontology.projectchronos.eu/subsystems/embedSensor",
            "skos:altLabel": "holds a sensor",
            "rdf:range": [
                {
                    "@id": "http://ontology.projectchronos.eu/sensors/Detector"
                }
            ]
        },
        {
            "skos:prefLabel": "the environment in which a device or a system of devices is designed to work",
            "@type": [
                {
                    "@id": "http://www.w3.org/2002/07/owl#AsymmetricProperty"
                },
                {
                    "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/spacecraft/isDeployedIn",
            "rdf:label": "isDeployedIn"
        }
    ],
    "@type": {
        "@id": "http://www.w3.org/2002/07/owl#Ontology"
    },
    "@id": "",
    "rdf:comment": "A space vessel is described as made of two components: a set of devices called BUS and a set of one or more DETECTORS (see /sensors/Detector)",
    "@context": {
        "schema": "https://schema.org/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "defines": {
            "@reverse": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"
        },
        "@base": "http://ontology.projectchronos.eu/spacecraft",
        "chronos": "http://ontology.projectchronos.eu/chronos/",
        "dbpedia": "http://live.dbpedia.org/ontology/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "spacecraft": "http://ontology.projectchronos.eu/spacecraft/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "engineering": "http://ontology.projectchronos.eu/engineering/"
    },
    "rdf:label": "Objects and properties to describe systems and subsystems of devices and structures needed to fly a spacecraft, including structure and platform. Words separated by _ has to be read as separated concepts, camelCase in they are the same concepts (see umbel.org for this norm)"
}
