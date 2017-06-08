subsystem_apidoc = {
    "@type": "ApiDocumentation",
    "title": "The name of the API",
    "supportedClass": [
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
                    "returns": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
                    "description": "null",
                    "@id": "_:cubicMillimeters_create",
                    "method": "POST",
                    "label": "Creates a new cubicMillimeters entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the cubicMillimeters entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
                    "returns": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
                    "description": "null",
                    "@id": "_:cubicMillimeters_replace",
                    "method": "PUT",
                    "label": "Replaces an existing cubicMillimeters entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:cubicMillimeters_delete",
                    "method": "DELETE",
                    "label": "Deletes a cubicMillimeters entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the cubicMillimeters entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters",
                    "description": "null",
                    "@id": "_:cubicMillimeters_retrieve",
                    "method": "GET",
                    "label": "Retrieves a cubicMillimeters entity"
                }
            ],
            "title": "cubicMillimeters",
            "description": "unit of measure for volume",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
                    "description": "null",
                    "@id": "_:Spacecraft_Detector_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Detector entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Detector entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
                    "description": "null",
                    "@id": "_:Spacecraft_Detector_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Detector entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Detector_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Detector entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Detector entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
                    "description": "null",
                    "@id": "_:Spacecraft_Detector_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Detector entity"
                }
            ],
            "title": "Spacecraft_Detector",
            "description": "A space detector is a sensor supported by another device that let it collect data, that is deployed into a spacecraft and works outside Earth lower atmosphere",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/objective"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/isComponentOf"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVoltage"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
                    "description": "null",
                    "@id": "_:Spacecraft_Propulsion._create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Propulsion. entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Propulsion. entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
                    "description": "null",
                    "@id": "_:Spacecraft_Propulsion._replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Propulsion. entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Propulsion._delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Propulsion. entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Propulsion. entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
                    "description": "null",
                    "@id": "_:Spacecraft_Propulsion._retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Propulsion. entity"
                }
            ],
            "title": "Spacecraft_Propulsion.",
            "description": "Complex devices-subsystems used for impelling (processes of applying a force which results in translational motion) a spacecraft, in the specific http://umbel.org/umbel/rc/ProjectilePropelling",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/typeOfPropellant"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
                    "description": "null",
                    "@id": "_:Spacecraft_PrimaryPower._create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_PrimaryPower. entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_PrimaryPower. entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
                    "description": "null",
                    "@id": "_:Spacecraft_PrimaryPower._replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_PrimaryPower. entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_PrimaryPower._delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_PrimaryPower. entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_PrimaryPower. entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
                    "description": "null",
                    "@id": "_:Spacecraft_PrimaryPower._retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_PrimaryPower. entity"
                }
            ],
            "title": "Spacecraft_PrimaryPower.",
            "description": "Complex devices-subsystems used for collecting energy.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasEfficiency"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVoltage"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
                    "description": "null",
                    "@id": "_:Spacecraft_BackupPower_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_BackupPower entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_BackupPower entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
                    "description": "null",
                    "@id": "_:Spacecraft_BackupPower_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_BackupPower entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_BackupPower_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_BackupPower entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_BackupPower entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
                    "description": "null",
                    "@id": "_:Spacecraft_BackupPower_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_BackupPower entity"
                }
            ],
            "title": "Spacecraft_BackupPower",
            "description": "Complex devices-subsystems used for storing energy.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Thermal entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Thermal entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Thermal entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Thermal entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Thermal entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Thermal entity"
                }
            ],
            "title": "Spacecraft_Thermal",
            "description": "Shields, shells or any device insulation from/reflecting radiation exploiting emission and absorption events",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_PassiveDevice_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Thermal_PassiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Thermal_PassiveDevice entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_PassiveDevice_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Thermal_PassiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_PassiveDevice_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Thermal_PassiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Thermal_PassiveDevice entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_PassiveDevice_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Thermal_PassiveDevice entity"
                }
            ],
            "title": "Spacecraft_Thermal_PassiveDevice",
            "description": "They are passive because they mostly transform radiation into heating/cooling ",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_PassiveDevice"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_ActiveDevice_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Thermal_ActiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Thermal_ActiveDevice entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_ActiveDevice_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Thermal_ActiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_ActiveDevice_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Thermal_ActiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Thermal_ActiveDevice entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_Thermal_ActiveDevice_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Thermal_ActiveDevice entity"
                }
            ],
            "title": "Spacecraft_Thermal_ActiveDevice",
            "description": "Complex devices-subsystems used to protect sensors or electronic devices from over/under-heating, like refrigeration absorption.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal_ActiveDevice"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
                    "description": "null",
                    "@id": "_:Spacecraft_Structure_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Structure entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Structure entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
                    "description": "null",
                    "@id": "_:Spacecraft_Structure_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Structure entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Structure_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Structure entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Structure entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
                    "description": "null",
                    "@id": "_:Spacecraft_Structure_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Structure entity"
                }
            ],
            "title": "Spacecraft_Structure",
            "description": "It's the skeleton and framework of the spacecraft.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/standsMaxTemperature"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
                    "description": "null",
                    "@id": "_:Spacecraft_CDH_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_CDH entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_CDH entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
                    "description": "null",
                    "@id": "_:Spacecraft_CDH_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_CDH entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_CDH_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_CDH entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_CDH entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
                    "description": "null",
                    "@id": "_:Spacecraft_CDH_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_CDH entity"
                }
            ],
            "title": "Spacecraft_CDH",
            "description": "The DH system shall: Enable HK and science data flow \u2013 Housekeeping data (Temperatures, Pressures, Voltages, Currents, Status,...) \u2013 Attitude data \u2013 Payload data (e.g., Science data) - Receive and distribute commands - Perform TM and TC protocols - Distribute timing signals - Synchronization of data \u2013 Time stamping of data - Provide data storage - Execute commands and schedules - Control subsystems and payloads - Monitor spacecraft health - Make autonomous decisions - Perform data compression.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVoltage"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxClock"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinClock"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasDataStorage"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasDataStorageExternal"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasRAM"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxTemperature"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
                    "description": "null",
                    "@id": "_:Spacecraft_Communication_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_Communication entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Communication entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
                    "description": "null",
                    "@id": "_:Spacecraft_Communication_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_Communication entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_Communication_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_Communication entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_Communication entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication",
                    "description": "null",
                    "@id": "_:Spacecraft_Communication_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_Communication entity"
                }
            ],
            "title": "Spacecraft_Communication",
            "description": "Complex devices-subsystems used for transmitting/receiving radio waves.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/spacecraft/isSubsystemOf"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxTemperature"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Communication"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_AODCS entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_AODCS entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_AODCS entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_AODCS entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_AODCS entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_AODCS entity"
                }
            ],
            "title": "Spacecraft_AODCS",
            "description": "Complex devices-subsystems used to set the direction and the position of the spacecraft, it controls flight dynamics.",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "function",
                    "description": "The function and the objective what the device performs or make possible",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "subSystemType",
                    "description": "A property that references the subsystem to the kind of the devices it holds.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/subSystemType"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "isStandard",
                    "description": "A property that references the standard platform for which the subsystem has been designed.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/isStandard"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasVolume",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasVolume"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMinAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMinAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMaxAmpere",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMaxAmpere"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMass",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMass"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "minWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/minWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "maxWorkingTemperature",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/maxWorkingTemperature"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasPower",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasPower"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasSpecificImpulse",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasSpecificImpulse"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasMonetaryValue",
                    "description": "Amount of money it can be bought for, or an esteem of value.",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasMonetaryValue"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireInWith",
                    "description": "This device receive input from another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                },
                {
                    "@type": "SupportedProperty",
                    "title": "hasWireOutWith",
                    "description": "This device send output to another device",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireOutWith"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsytems/function"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/standsMaxTemperature"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_Active_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_AODCS_Active entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_AODCS_Active entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_Active_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_AODCS_Active entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_Active_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_AODCS_Active entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_AODCS_Active entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_Active_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_AODCS_Active entity"
                }
            ],
            "title": "Spacecraft_AODCS_Active",
            "description": "Do NOT use any additional power from the spacecraft generator",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_ActiveDevice"
        },
        {
            "@type": "Class",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_PassiveDevice_create",
                    "method": "POST",
                    "label": "Creates a new Spacecraft_AODCS_PassiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_AODCS_PassiveDevice entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_PassiveDevice_replace",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft_AODCS_PassiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [],
                    "expects": "null",
                    "returns": "null",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_PassiveDevice_delete",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft_AODCS_PassiveDevice entity"
                },
                {
                    "@type": "hydra:Operation",
                    "statusCodes": [
                        {
                            "description": "If the Spacecraft_AODCS_PassiveDevice entity wasn't found.",
                            "code": 404
                        }
                    ],
                    "expects": "null",
                    "returns": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice",
                    "description": "null",
                    "@id": "_:Spacecraft_AODCS_PassiveDevice_retrieve",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft_AODCS_PassiveDevice entity"
                }
            ],
            "title": "Spacecraft_AODCS_PassiveDevice",
            "description": "DO use any additional power from the spacecraft generator",
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "title": "manufacturer",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/manufacturer"
                },
                {
                    "@type": "SupportedProperty",
                    "writeonly": "false",
                    "readonly": "false",
                    "required": "false",
                    "property": "http://ontology.projectchronos.eu/subsystems/hasWireInWith"
                }
            ],
            "@id": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS_PassiveDevice"
        }
    ],
    "entrypoint": "URL of the API's main entry point",
    "description": "A short description of the API",
    "@context": "http://www.w3.org/ns/hydra/context.jsonld",
    "@id": "http://api.example.com/doc/",
    "possibleStatus": []
}
