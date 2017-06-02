"""Test script to enter data from random objects into old models(Depreciated)."""

from models import Property, Instance, Graph, engine, Classes, Terminal
from generator import gen_all_types
from sqlalchemy.orm import sessionmaker
import pdb
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
Session = sessionmaker(bind=engine)
session = Session()


for object_ in objects:
    class_name = keymap[object_["object"]["category"]]
    class_ = session.query(Classes).filter(Classes.name == class_name).one()

    resource = Instance(id=object_["id"], name=object_["name"], type_=class_.id)
    pdb.set_trace()
    session.add(resource)
    session.commit()

    for prop in object_["object"]:
        if prop != "category":
            property_ = session.query(Property).filter(Property.name == prop).one()

            value = Terminal(value=object_["object"][prop], unit="number")
            session.add(value)
            session.commit()

            triple = Graph(
                subject=resource,
                subject_type="INSTANCE",
                predicate=property_,
                object_id=value.id,
                object_type="TERMINAL"
            )
            triple_store.append(triple)
    pdb.set_trace()

    # Adding the objects and properties to the graph
    for prop in allowed_properties:
        triple = Graph(resource, prop, object_["object"][prop.name])
        triple_store.append(triple)

# Printing the graph in triple form
for triple in triple_store:
    print(triple.subject.name, triple.predicate.name, triple.object)
