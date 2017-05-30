"""Generate random data and create triples using objects."""

from models import Property, SubSysType, Resource, Graph
from generator import gen_all_types

keymap = {
    "communication": "Spacecraft_Communication",
    "propulsion": "Spacecraft_Propulsion",
    "detector": "Spacecraft_Detector",
    "primary power": "Spacecraft_PrimaryPower",
    "backup power": "Spacecraft_BackupPower",
    "thermal": "Spacecraft_Thermal",
    "structure":  "Spacecraft_Structure",
    "command and data": "Spacecraft_CDH",
    "attitude and orbit control": "Spacecraft_AODCS",
}


# Temporary storge for the Graph
triple_store = list()

# Random generated objects
objects = gen_all_types()

for object_ in objects:
    # Finding all allowed properties for given object
    allowed_properties = list()
    for prop in object_["object"]:
        allowed_properties.append(Property(prop))
    # Creating SubSystem object
    subsystem = SubSysType(keymap[object_["object"]["category"]], allowed_properties)
    # Creating Resource object using SubSystem object
    resource = Resource(id_=object_["id"], name=object_["name"], type_=subsystem)
    # Adding the objects and properties to the graph
    for prop in allowed_properties:
        triple = Graph(resource, prop, object_["object"][prop.name])
        triple_store.append(triple)

# Printing the graph in triple form
for triple in triple_store:
    print(triple.subject.name, triple.predicate.name, triple.object)
