astronomy = {
	"@context": {
		"@base": "http://ontology.projectchronos.eu/astronomy",
        "hydra": "http://www.w3.org/ns/hydra/context.jsonld",
		"schema": "https://schema.org/",
		"skos": "http://www.w3.org/2004/02/skos/core#",
		"owl": "http://www.w3.org/2002/07/owl#",
		"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
		"dbpedia": "http://live.dbpedia.org/ontology/",
		"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
		"astronomy": "http://ontology.projectchronos.eu/astronomy/",
		"defines": {
			"@reverse": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"
		},
		"chronos": "http://ontology.projectchronos.eu/chronos/"
	},
	"rdf:label": "Generic astronomical concepts ",
	"rdf:comment": "a set of concepts to be used to describe astronomical objects. Notes: 1. two different properties are applied for bodies orbiting a star (property \"orbiting\") and orbiting a planet (property \"orbitsPlanet\") - 2. PlanetaryBody entity is a wider group for any object subject permanently to the gravity of a Planet. Planet entity is for the planet itself",
	"@type": "http://www.w3.org/2002/07/owl#Ontology",
	"defines": [{
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/AstronomicalObject.n3"
		},
		"rdf:label": "AstronomicalObject",
		"rdf:comment": "an astronomical body (from a natural satellite size up) or a group of astronomical body",
		"@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "Planetary_system",
		"rdf:comment": "Solar System is a planetary system - see solarsystem vocabulary",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/data/Planetary_system.ntriples"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Planetary_system"
	}, {
		"rdf:label": "Star",
		"rdf:comment": "a star",
		"@type": "hydra:Class",
		"owl:sameAs": [{
			"@id": "http://umbel.org/umbel/rc/Star.n3"
		}, {
			"@id": "http://sw.opencyc.org/concept/Mx4rvVi80ZwpEbGdrcN5Y29ycA"
		}, {
			"@id": "http://live.dbpedia.org/data/Star.n3"
		}],
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Star"
	}, {
		"skos:altLabel": "a general astronomical object with the characteristics of a planet or any natural object under gravitational influence of a planet",
		"rdf:label": "PlanetaryBody",
		"rdf:comment": "a document representing a general planet-shaped body or natural satellite or dust or rock or macroscopic particle of matter",
		"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody",
		"@type": "hydra:Class"
	}, {
		"skos:altLabel": "a general astronomical object with the characteristics of a planet",
		"rdf:label": "Planet",
		"rdf:comment": "a document representing a general planet-shaped astronomical body",
		"@type": "hydra:Class",
		"owl:sameAs": [{
			"@id": "http://sw.opencyc.org/concept/Mx4rvVjRL5wpEbGdrcN5Y29ycA"
		}, {
			"@id": "http://live.dbpedia.org/data/Planet.n3"
		}],
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Planet"
	}, {
		"rdf:label": "orbiting",
		"rdf:comment": "this property describe the generic astronomical object-object gravitational interaction",
		"@type": "http://www.w3.org/2002/07/owl#ObjectProperty",
		"owl:sameAs": {
			"@id": "http://sw.opencyc.org/concept/Mx4rvmlCvZwpEbGdrcN5Y29ycA"
		},
		"rdf:domain": {
			"@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
		},
		"rdf:range": {
			"@id": "http://ontology.projectchronos.eu/astronomy/Star"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/orbiting"
	}, {
		"rdf:label": "orbitsPlanet",
		"rdf:domain": [{
			"@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
		}, {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		}],
		"@type": "http://www.w3.org/2002/07/owl#ObjectProperty",
		"rdf:comment": "this property describe the Moon-Planet gravitational interaction",
		"rdf:range": [{
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		}, {
			"@id": " http://ontology.projectchronos.eu/astronomy/DwarfPlanet"
		}],
		"rdfs:subClassOf": {
			"@id": ""
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/orbitsPlanet"
	}, {
		"rdfs:sameAs": [{
			"@id": "http://umbel.org/umbel/rc/SubplanetaryStellarOrbiter.n3"
		}, {
			"@id": "http://live.dbpedia.org/data/Asteroid.ntriples"
		}],
		"rdf:label": "Asteroid",
		"rdf:comment": "a document representing an asteroid",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/data/Asteroid.ntriples"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Asteroid"
	}, {
		"rdfs:sameAs": [{
			"@id": "http://umbel.org/umbel/rc/SubplanetaryStellarOrbiter.n3"
		}, {
			"@id": "http://live.dbpedia.org/data/Meteoroid.ntriples"
		}],
		"rdf:label": "Meteoroid",
		"rdf:comment": "a document representing a meteoroid",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/Meteoroid.n3"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Meteoroid"
	}, {
		"rdfs:sameAs": [{
			"@id": "http://umbel.org/umbel/rc/SubplanetaryStellarOrbiter.n3"
		}, {
			"@id": "http://live.dbpedia.org/data/Comet.ntriples"
		}],
		"rdf:label": "Comet",
		"rdf:comment": "a document representing a comet",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/Comet.n3"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Comet"
	}, {
		"owl:sameAs": [{
			"@id": "http://umbel.org/umbel/rc/MoonOfAPlanet.n3"
		}, {
			"@id": "http://live.dbpedia.org/data/Natural_satellite.ntriples"
		}, {
			"@id": "http://sw.opencyc.org/concept/Mx4rvfn7-pwpEbGdrcN5Y29ycA"
		}],
		"rdf:label": "Natural_satellite",
		"rdf:comment": "a document representing a natural satellite or moon",
		"@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "TerrestrialPlanet",
		"rdf:comment": "a document representing a solid/rocky planet",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/TerrestrialPlanet.n3"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet"
	}, {
		"rdf:label": "SolidPlanetaryBody",
		"rdf:comment": "planet composed primarily of solid substances",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/SolidPlanetaryBody.n3"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/SolidPlanetaryBody"
	}, {
		"rdf:label": "IcyPlanetaryBody",
		"rdf:comment": "a document representing an icy body",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/IcyPlanetaryBody.n3"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/IcyPlanetaryBody"
	}, {
		"rdf:label": "Ice_giant",
		"rdf:comment": "a gas giant with less helium/hydrogen and more 'ices', Uranus and Neputne subclass",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/data/Ice_giant.ntriples"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/GasGiant"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Ice_giant"
	}, {
		"rdf:label": "GasGiant",
		"rdf:comment": "a Jovian planet, a document representing a Jovian planet",
		"@id": "http://ontology.projectchronos.eu/astronomy/GasGiant",
		"@type": "hydra:Class",
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/GasGiant.n3"
		}
	}, {
		"rdf:label": "DwarfPlanet",
		"rdf:comment": "a trans-neptunian object with planet-like size",
		"@id": "http://ontology.projectchronos.eu/astronomy/DwarfPlanet",
		"@type": "hydra:Class",
		"astronomy:orbiting": {
			"@id": "http://ontology.projectchronos.eu/astronomy/Sun"
		},
		"rdfs:subClassOf": {
			"@id": "http://umbel.org/umbel/rc/SubplanetaryStellarOrbiter.n3"
		},
		"@owl:sameAs": {
			"@id": " http://live.dbpedia.org/data/Dwarf_planet.ntriples"
		}
	}, {
		"rdf:label": "RockyPlanetaryBody",
		"rdf:comment": "a document representing a rocky body",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/RockyPlanetaryBody.n3"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/RockyPlanetaryBody"
	}, {
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/SubplanetaryStellarOrbiter.n3"
		},
		"rdf:label": "SubplanetaryStellarOrbiter",
		"rdf:comment": "a smaller body orbiting around stars or planets, a document representing smaller body orbiting around stars or planets",
		"@id": "http://ontology.projectchronos.eu/astronomy/SubplanetaryStellarOrbiter",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "FluidPlanetaryBody",
		"rdf:comment": "a document representing a non-solid planet",
		"@type": "hydra:Class",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/FluidPlanetaryBody.n3"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/FluidPlanetaryBody"
	}, {
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/AstronomicalObservatory.n3"
		},
		"rdf:label": "AstronomicalObservatory",
		"rdf:comment": "a document representing an astronomical observatory",
		"@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObservatory",
		"@type": "hydra:Class"
	}, {
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/ontology/CelestialBody.ntriples"
		},
		"rdf:label": "CelestialBody",
		"rdf:comment": "a document representing a generic celestial body",
		"@id": "http://ontology.projectchronos.eu/astronomy/CelestialBody",
		"@type": "hydra:Class"
	}, {
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/ontology/Outer_space.ntriples"
		},
		"rdf:label": "Outer_space",
		"rdf:comment": "a document representing the open space outside atmosphere, from Low Earth Orbit to Extra Galactic Space",
		"@id": "http://ontology.projectchronos.eu/astronomy/Outer_space",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "PlanetaryScience",
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/data/Planetary_science.ntriples"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/FieldOfResearch"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryScience",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "AtmosphericScience",
		"owl:sameAs": {
			"@id": "http://umbel.org/umbel/rc/AtmosphericScience.n3"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/PlanetaryScience"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/AtmosphericScience",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "Cosmology",
		"owl:sameAs": [{
			"@id": "http://umbel.org/umbel/rc/Cosmology.n3"
		}, {
			"@id": "http://live.dbpedia.org/data/Cosmology.ntriples"
		}],
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/FieldOfResearch"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/Cosmology",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "ExtragalacticAstronomy",
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/data/Extragalactic_astronomy.ntriples"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/FieldOfResearch"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/ExtragalacticAstronomy",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "GalacticAstronomy",
		"owl:sameAs": {
			"@id": "http://live.dbpedia.org/data/Galactic_astronomy.ntriples"
		},
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/FieldOfResearch"
		},
		"@id": "http://ontology.projectchronos.eu/astronomy/GalacticAstronomy",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "PlanetaryAstronomy",
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/PlanetaryScience"
		},
		"@id": "http://ontology.projectchronos.eu/sensors/PlanetaryAstronomy",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "PlanetaryGeology",
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/PlanetaryScience"
		},
		"@id": "http://ontology.projectchronos.eu/sensors/PlanetaryGeology",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "SolarAstronomy",
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/FieldOfResearch"
		},
		"@id": "http://ontology.projectchronos.eu/sensors/SolarAstronomy",
		"@type": "hydra:Class"
	}, {
		"rdf:label": "StellarAstronomy",
		"rdfs:subClassOf": {
			"@id": "http://ontology.projectchronos.eu/sensors/FieldOfResearch"
		},
		"@id": "http://ontology.projectchronos.eu/sensors/StellarAstronomy",
		"@type": "hydra:Class"
	}],
	"@id": ""
}

solarsystem = {
    "@context": {
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "astronomy": "http://ontology.projectchronos.eu/astronomy/",
        "defines": {
            "@reverse": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"
        },
        "chronos": "http://ontology.projectchronos.eu/chronos/",
        "dbpedia": "http://live.dbpedia.org/ontology/",
        "schema": "https://schema.org/",
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "@base": "http://ontology.projectchronos.eu/solarsystem"
    },
    "rdf:label": "A description of the Solar System taking major classes from DBpedia and Umbel",
    "@type": "http://www.w3.org/2002/07/owl#Ontology",
    "@id": "",
    "defines": [{
        "rdf:label": "Solar_System",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Solar_System",
        "@type": "http://ontology.projectchronos.eu/astronomy/Planetary_system",
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/SolarSystem"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/SolarSystem"
        }]
    }, {
        "rdf:label": "Sun",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Sun",
        "@type": "http://ontology.projectchronos.eu/astronomy/Star",
        "owl:sameAs": [{
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/Sun"
        }, {
            "@id": "http://live.dbpedia.org/data/Sun.ntriples"
        }]
    }, {
        "rdf:label": "Mercury",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Mercury",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/SolidPlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetMercury"
        }, {
            "@id": "http://live.dbpedia.org/data/Mercury_(planet).ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetMercury"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Venus",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Venus",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/SolidPlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetVenus"
        }, {
            "@id": "http://live.dbpedia.org/data/Venus_(planet).ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetVenus"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Earth",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Earth",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/SolidPlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetEarth"
        }, {
            "@id": "http://live.dbpedia.org/data/Earth.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetEarth"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Moon",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Moon",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/MoonOfEarth"
        }, {
            "@id": "http://live.dbpedia.org/data/Moon.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/MoonOfEarth"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Earth"
        }
    }, {
        "rdf:label": "Mars",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Mars",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/SolidPlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetMars"
        }, {
            "@id": "http://live.dbpedia.org/data/Mars.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetMars"
        }],
        "astronomy:orbiting ": {
            "@id ": "http: //ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Phobos",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Phobos",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/http://umbel.org/umbel/rc/Phobos_MoonOfMars"
        }, {
            "@id": "http://live.dbpedia.org/data/Phobos_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Mars"
        }
    }, {
        "rdf:label": "Deimos",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Deimos",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/http://umbel.org/umbel/rc/Deimos_MoonOfMars"
        }, {
            "@id": "http://live.dbpedia.org/data/Deimos_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Mars"
        }
    }, {
        "rdf:label": "Asteroids_belt",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Asteroid_belt",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/AsteroidBelt"
        }, {
            "@id": "http://live.dbpedia.org/data/Asteroid_belt.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/AsteroidBelt"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Jupiter",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/GasGiant"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetJupiter"
        }, {
            "@id": "http://live.dbpedia.org/data/Jupiter.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetJupiter"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Metis",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Metis",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Metis_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Adrastea",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Adrastea",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Adrastea_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Amalthea",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Amalthea",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Amalthea_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Thebe",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Thebe",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Thebe_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Io",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Io",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Io_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter "
        }
    }, {
        "rdf:label": "Europa",
        "@id": "http: //ontology.projectchronos.eu/solarsystem/Europa",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Europa_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Ganymede",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Ganymede",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Ganymede_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Callisto",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Callisto",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Callisto_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Themisto",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Themisto",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Themisto_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Leda",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Leda",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Leda_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Himalia",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Himalia",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Himalia_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Lysithea",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Lysithea",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Lysithea_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Elara",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Elara",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Elara_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Carpo",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Carpo",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Carpo_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Euporie",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Euporie",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Euporie_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "OtherMoonsOfJupiter",
        "@id": "http://ontology.projectchronos.eu/solarsystem/OtherMoonsOfJupiter",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Moons_of_Jupiter.ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Jupiter"
        }
    }, {
        "rdf:label": "Saturn",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Saturn",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/GasGiant"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetSaturn"
        }, {
            "@id": "http://live.dbpedia.org/data/Saturn.ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Mimas",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Mimas",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Mimas_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": "http://ontology.projectchronos.eu/solarsystem/Saturn"
    }, {
        "rdf:label": "Enceladus",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Enceladus",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Enceladus_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Saturn"
        }
    }, {
        "rdf:label": "Dione",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Dione",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Dione_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Saturn"
        }
    }, {
        "rdf:label": "Rhea",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Rhea",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Rhea_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Saturn"
        }
    }, {
        "rdf:label": "Titan",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Titan",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Titan_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Saturn"
        }
    }, {
        "rdf:label": "Iapetus",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Iapetus",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Iapetus_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Saturn"
        }
    }, {
        "rdf:label": "Uranus",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/GasGiant"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Ice_giant"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetUranus"
        }, {
            "@id": "http://live.dbpedia.org/data/Uranus.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetUranus"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Cordelia",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Cordelia",
        "@type": [{
            "@id": "http: //ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Cordelia_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Ophelia",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Ophelia",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Ophelia_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Bianca",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Bianca",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Bianca_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Cressida",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Cressida",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Cressida_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Desdemona",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Desdemona",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Desdemona_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Juliet",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Juliet",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Juliet_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Portia",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Portia",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Portia_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Rosalind",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Rosalind",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Rosalind_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Cupid",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Cupid",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Cupid_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Belinda",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Belinda",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Belinda_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Perdita",
        "@id": "http: //ontology.projectchronos.eu/solarsystem/Perdita",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Perdita_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Puck",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Puck",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Puck_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Mab",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Mab",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Mab_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Miranda",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Miranda",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Miranda_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Ariel",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Ariel",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Ariel_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Umbriel",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Umbriel",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Umbriel_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Titania",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Titania",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Titania_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Oberon",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Oberon",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Oberon_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Uranus"
        }
    }, {
        "rdf:label": "Neptune",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/Ice_giant"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/GasGiant"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Planet"
        }],
        "owl:sameAs": [{
            "@id": "http://umbel.org/umbel/rc/PlanetNeptune"
        }, {
            "@id": "http://live.dbpedia.org/data/Neptune.ntriples"
        }, {
            "@id": "http://sw.opencyc.org/2012/05/10/concept/en/PlanetNeptune"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Naiad",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Naiad",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite "
        }],
        "owl:sameAs ": [{
            "@id": "http: //live.dbpedia.org/data/Naiad_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Thalassa",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Thalassa",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Thalassa_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Despina",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Despina",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Despina_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Galatea",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Galatea",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Galatea_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Larissa",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Larissa",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Larissa_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Proteus",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Proteus",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Proteus_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Triton",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Triton",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Triton_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Nereid",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Nereid",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Nereid_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Halimede",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Halimede",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Halimede_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Sao",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Sao",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Sao_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Laomedeia",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Laomedeia",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody "
        }, {
            "@id": "http: //ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Laomedeia_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Psamathe",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Psamathe",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Psamathe_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Neso",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Neso",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Neso_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Neptune"
        }
    }, {
        "rdf:label": "Ceres",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Ceres",
        "@type": {
            "@id": "http://ontology.projectchronos.eu/astronomy/DwarfPlanet"
        },
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Ceres_(dwarf_planet).ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Pluto",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Pluto",
        "@type": "http://ontology.projectchronos.eu/astronomy/DwarfPlanet",
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Pluto.ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Charon",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Charon",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Charon_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Pluto"
        }
    }, {
        "rdf:label": "Styx",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Styx",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Styx_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Pluto"
        }
    }, {
        "rdf:label": "Nix",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Nix",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Nix_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Pluto"
        }
    }, {
        "rdf:label": "Kerberos",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Kerberos",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Kerberos_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Pluto"
        }
    }, {
        "rdf:label": "Hydra",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Hydra",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Hydra_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Pluto"
        }
    }, {
        "rdf:label": "Haumea",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Haumea",
        "@type": "http://ontology.projectchronos.eu/astronomy/DwarfPlanet",
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Haumea.ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Haumea_I_and_II",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Haumea_I_and_II",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Moons_of_Haumea.ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Haumea"
        }
    }, {
        "rdf:label": "Makemake",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Makemake",
        "@type": "http://ontology.projectchronos.eu/astronomy/DwarfPlanet",
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Makemake.ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Eris",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Eris",
        "@type": "http://ontology.projectchronos.eu/astronomy/DwarfPlanet",
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Eris_(dwarf_planet).ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "rdf:label": "Dysnomia",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Dysnomia",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/PlanetaryBody"
        }, {
            "@id": "http://ontology.projectchronos.eu/astronomy/Natural_satellite"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Dysnomia_(moon).ntriples"
        }],
        "astronomy:orbitsPlanet": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Eris"
        }
    }, {
        "rdf:label": "Trans-Neptunian_object",
        "@id": "http://ontology.projectchronos.eu/solarsystem/Trans-Neptunian_object",
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
        }],
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Trans-Neptunian_object.ntriples"
        }],
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
        }],
        "rdf:label": "Kuiper_belt",
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Kuiper_belt.ntriples"
        }],
        "@id": "http://ontology.projectchronos.eu/solarsystem/Kuiper_belt",
        "rdfs:subClassOf": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Trans-Neptunian_object"
        },
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }, {
        "@type": [{
            "@id": "http://ontology.projectchronos.eu/astronomy/AstronomicalObject"
        }],
        "rdf:label": "Oort_cloud",
        "owl:sameAs": [{
            "@id": "http://live.dbpedia.org/data/Oort_cloud.ntriples"
        }],
        "@id": "http://ontology.projectchronos.eu/solarsystem/Oort_cloud",
        "rdfs:subClassOf": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Trans-Neptunian_object"
        },
        "astronomy:orbiting": {
            "@id": "http://ontology.projectchronos.eu/solarsystem/Sun"
        }
    }],
    "rdf:comment": "The major Astronomical Bodies in the Solar System are described in terms of what orbits what. Inherited from OpenCyc, DBpedia and Umbel"
}