"""Subsystems vocabulary from http://ontology.projectchronos.eu/subsystems/?format=jsonld."""
# Listed classes:
#     "Spacecraft_Communication":  models.Classes(name="Spacecraft_Communication"),
#     "Spacecraft_Propulsion":  models.Classes(name="Spacecraft_Propulsion"),
#     "Spacecraft_Detector":  models.Classes(name="Spacecraft_Detector"),
#     "Spacecraft_PrimaryPower":  models.Classes(name="Spacecraft_PrimaryPower"),
#     "Spacecraft_BackupPower":  models.Classes(name="Spacecraft_BackupPower"),
#     "Spacecraft_Thermal":  models.Classes(name="Spacecraft_Thermal"),
#     "Spacecraft_Structure":  models.Classes(name="Spacecraft_Structure"),
#     "Spacecraft_CDH":  models.Classes(name="Spacecraft_CDH"),
#     "Spacecraft_AODCS":  models.Classes(name="Spacecraft_AODCS"),
#     "Spacecraft":  models.Classes(name="Spacecraft"),
#     "Subsystem_Spacecraft":  models.Classes(name="Subsystem_Spacecraft"),  # all the subsystems types, except detectors (or experiments)
#     "Payload_Spacecraft":  models.Classes(name="Payload_Spacecraft")  # Detectors are payload not strictly subssytems


subsystem_data = {
    "defines": [
        {
            "@type": [
                {
                    "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/manufacturer",
            "rdf:label": "manufacturer",
            "owl:sameAs": {
                "@id": "http://sw.opencyc.org/2012/05/10/concept/Mx8Ngh4rvkpzWpwpEbGdrcN5Y29ycB4rvViQlZwpEbGdrcN5Y29ycA"
            }
        },
        {
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
            "rdf:comment": "The function and the objective what the device performs or make possible",
            "rdf:label": "function",
            "@id": "http://ontology.projectchronos.eu/subsystems/function",
            "skos:altLabel": "is used for"
        },
        {
            "@type": "http://www.w3.org/2002/07/owl#ObjectProperty",
            "@id": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
            "rdf:comment": "unit of measure for volume",
            "rdf:label": "cubicMillimeters"
        },
        {
            "skos:prefLabel": "A property that references the subsystem to the kind of the devices it holds.",
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:comment": "Every subsystem contains an homogeneous group of devices.",
            "rdf:label": "subSystemType",
            "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
        },
        {
            "skos:prefLabel": "A property that references the standard platform for which the subsystem has been designed.",
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:comment": "There are many different standards that imply quantitative and qualitative differences",
            "rdf:label": "isStandard",
            "@id": "http://ontology.projectchronos.eu/subsystems/isStandard"
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "hasVolume",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasVolume",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Volume"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Volume.ntriples"
                },
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/Mx4rvVju5JwpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "hasMinAmpere",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Ampere"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Ampere.ntriples"
                },
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/Mx4rvVieG5wpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "hasMaxAmpere",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Ampere"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Ampere.ntriples"
                },
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/Mx4rvVieG5wpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "hasMass",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasMass",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Mass"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Mass.ntriples"
                },
                {
                    "@id": "http://schema.org/Mass"
                },
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/Mx4rvVjb5pwpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "minWorkingTemperature",
            "rdf:range": [
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/en/DegreeCelsius"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Temperature"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Temperature.ntriples"
                },
                {
                    "@id": "http://sw.opencyc.org/concept/Mx4rvVixf5wpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "maxWorkingTemperature",
            "rdf:range": [
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/en/DegreeCelsius"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Temperature"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Temperature.ntriples"
                },
                {
                    "@id": "http://sw.opencyc.org/concept/Mx4rvVixf5wpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "hasPower",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasPower",
            "owl:sameAs": [
                {
                    "@id": "http://umbel.org/umbel/rc/Power"
                },
                {
                    "@id": "http://live.dbpedia.org/data/Power_(physics).ntriples"
                },
                {
                    "@id": "http://sw.opencyc.org/2012/05/10/concept/Mx4rvVjcq5wpEbGdrcN5Y29ycA"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:label": "hasSpecificImpulse",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse",
            "owl:sameAs": {
                "@id": "http://live.dbpedia.org/data/Specific_impulse.ntriples"
            }
        },
        {
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft_Detector"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/holdsSensor",
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:label": "holdsSensor"
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:comment": "Amount of money it can be bought for, or an esteem of value.",
            "rdf:label": "hasMonetaryValue",
            "rdf:range": [
                {
                    "@id": "http://www.w3.org/2001/XMLSchema#float"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue",
            "owl:sameAs": [
                {
                    "@id": "http://live.dbpedia.org/data/Price.ntriples"
                },
                {
                    "@id": "http://umbel.org/umbel/rc/MonetaryValue"
                },
                {
                    "@id": "http://schema.org/PriceSpecification"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:comment": "This device receive input from another device",
            "rdf:label": "hasWireInWith",
            "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith",
            "rdf:range": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ]
        },
        {
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ],
            "rdf:comment": "This device send output to another device",
            "rdf:label": "hasWireOutWith",
            "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith",
            "rdf:range": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                }
            ]
        },
        {
            "rdf:domain": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft_Propulsion"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/typeOfPropellant",
            "rdf:label": "typeOfPropellant",
            "@type": {
                "@id": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            "rdf:comment": "Type of fueling used by a spacecraft rocket engine"
        },
        {
            "skos:prefLabel": "Any scientific instrument carried by a space probe or an artificial satellite",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
            "chronos:relConcept": {
                "@id": "http://hypermedia.projectchronos.eu/data/dbpediadocs/sensor"
            },
            "rdf:comment": "A space detector is a sensor supported by another device that let it collect data, that is deployed into a spacecraft and works outside Earth lower atmosphere",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Payload_Spacecraft"
            },
            "rdf:label": "Spacecraft_Detector",
            "rdfs:subClassOf": [
                {
                    "@id": "http://umbel.org/umbel/rc/Sensor_Device"
                },
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/SubSystems_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/objective"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/isComponentOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Payload_Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasVoltage"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                }
            ]
        },
        {
            "skos:prefLabel": "The set of subsystems needed to make a spacecraft moving in space",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
            "chronos:relConcept": {
                "@id": "http://hypermedia.projectchronos.eu/data/dbpediadocs/propulsion"
            },
            "rdf:comment": "Complex devices-subsystems used for impelling (processes of applying a force which results in translational motion) a spacecraft, in the specific http://umbel.org/umbel/rc/ProjectilePropelling",
            "spacecraft:isComponentOf": "http://ontology.projectchronos.eu/spacecraft/Spacecraft",
            "rdf:label": "Spacecraft_Propulsion",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/ProjectilePropelling"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/typeOfPropellant"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/RocketEngine"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "The set of subsystems needed to make a spacecraft to collect energy to operate",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
            "rdf:comment": "Complex devices-subsystems used for collecting energy.",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_PrimaryPower",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/ElectricalPowerGeneration"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasEfficiency"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasVoltage"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/ElectricalDevice"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "The set of subsystems needed to make a spacecraft to store energy from the primary power source.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
            "rdf:comment": "Complex devices-subsystems used for storing energy.",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_BackupPower",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://live.dbpedia.org/data/rc/Energy_storage.ntriples"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/ElectricalDevice"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "Artifacts or devices used to maintain the temperature of spacecraft's subsystems and payloads into a given range, to permit nominal and survival mode for all the duration of the mission .",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
            "rdf:comment": "Shields, shells or any device insulation from/reflecting radiation exploiting emission and absorption events",
            "rdf:label": "Spacecraft_Thermal",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://live.dbpedia.org/data/Process_control.ntriples"
                    }
                }
            ]
        },
        {
            "skos:prefLabel": "Device of of class Thermal that does NOT consume energy from the spacecraft power source.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice",
            "rdf:comment": "They are passive because they mostly transform radiation into heating/cooling ",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_Thermal_PassiveDevice",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/PhysicalDevice"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                }
            ]
        },
        {
            "skos:prefLabel": "Device that of class Thermal that consumes energy from the spacecraft power source.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice",
            "rdf:comment": "Complex devices-subsystems used to protect sensors or electronic devices from over/under-heating, like refrigeration absorption.",
            "rdf:label": "Spacecraft_Thermal_ActiveDevice",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft_Thermal"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/PoweredDevice"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "Artifacts or rigid devices used to create a supporting structure for all the others devices.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
            "rdf:comment": "It's the skeleton and framework of the spacecraft.",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_Structure",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://live.dbpedia.org/data/Structural_system.ntriples"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/standsMaxTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/PhysicalDevice"
                    }
                }
            ]
        },
        {
            "skos:prefLabel": "Command and Data Handling, it is the device that connects the other devices, it processes and deliver information.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
            "rdf:comment": "The DH system shall: Enable HK and science data flow \u2013 Housekeeping data (Temperatures, Pressures, Voltages, Currents, Status,...) \u2013 Attitude data \u2013 Payload data (e.g., Science data) - Receive and distribute commands - Perform TM and TC protocols - Distribute timing signals - Synchronization of data \u2013 Time stamping of data - Provide data storage - Execute commands and schedules - Control subsystems and payloads - Monitor spacecraft health - Make autonomous decisions - Perform data compression.",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_CDH",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://umbel.org/umbel/rc/InformationTransferEvent"
                        },
                        {
                            "@id": "http://live.dbpedia.org/data/Electronic_data_processing.ntriples"
                        },
                        {
                            "@id": "http://live.dbpedia.org/data/Process_control.ntriples"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasVoltage"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMaxClock"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMinClock"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasDataStorage"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasDataStorageExternal"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasRAM"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMinTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMaxTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/Computer_hardware"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "It handles communication from/to ground base or other spacecraft.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
            "chronos:relConcept": {
                "@id": "http://hypermedia.projectchronos.eu/data/dbpediadocs/telecommunication"
            },
            "rdf:comment": "Complex devices-subsystems used for transmitting/receiving radio waves.",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_Communication",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://live.dbpedia.org/data/Transmitting.ntriples"
                        },
                        {
                            "@id": "http://umbel.org/umbel/rc/Receiving"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMinTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasMaxTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/ElectronicDevice"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "Attitude and Orbit Determination Control",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
            "rdf:comment": "Complex devices-subsystems used to set the direction and the position of the spacecraft, it controls flight dynamics.",
            "spacecraft:isComponentOf": {
                "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft"
            },
            "rdf:label": "Spacecraft_AODCS",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Subsystem_Spacecraft"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsytems/function"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://live.dbpedia.org/data/Flight_dynamics_(spacecraft).ntriples"
                        },
                        {
                            "@id": "http://live.dbpedia.org/data/Attitude_control.ntriples"
                        },
                        {
                            "@id": "http://live.dbpedia.org/data/Process_control.ntriples"
                        }
                    ]
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/standsMaxTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:minCardinality": 1
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": {
                        "@id": "http://umbel.org/umbel/rc/ElectronicDevice"
                    }
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "AODCS that do not use any power from the spacecraft power to work.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice",
            "rdf:comment": "Do NOT use any additional power from the spacecraft generator",
            "rdf:label": "Spacecraft_AODCS_Active",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft_AODCS"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower"
                        },
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                }
            ]
        },
        {
            "skos:prefLabel": "AODCS that do not use any power from the spacecraft power to work.",
            "@type": "http://www.w3.org/2002/07/owl#Class",
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice",
            "rdf:comment": "DO use any additional power from the spacecraft generator",
            "rdf:label": "Spacecraft_AODCS_PassiveDevice",
            "rdfs:subClassOf": [
                {
                    "@id": "http://ontology.projectchronos.eu/spacecraft/Spacecraft_AODCS"
                },
                {
                    "owl:onProperty": {
                        "@id": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                    },
                    "@type": "http://www.w3.org/2002/07/owl#Restriction",
                    "owl:hasValue": [
                        {
                            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
                        }
                    ]
                }
            ]
        }
    ],
    "@type": "http://www.w3.org/2002/07/owl#Ontology",
    "@id": "",
    "rdf:comment": "These ontology contains classes of different subsystems present in a spacecraft.",
    "@context": {
        "defines": {
           "@reverse": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"
        },
        "chronos": "http://ontology.projectchronos.eu/chronos/",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "xml": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "dbpedia": "http://live.dbpedia.org/ontology/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "@base": "http://ontology.projectchronos.eu/subsystems",
        "owl": "http://www.w3.org/2002/07/owl#",
        "spacecraft": "http://ontology.projectchronos.eu/spacecraft/"
    },
    "rdf:label": "Subsystems that run tasks that are needed for the spacecraft to be working and fulfilling the objectives of the mission. Words separated by _ has to be read as separated concepts, camelCase in they are the same concepts (see umbel.org for this norm)"
}
