"""Test script to enter data from random objects into old models(Depreciated)."""

from models import Property, Instance, Graph, engine, RDFClass, Terminal
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
    print(class_name)
    class_ = session.query(RDFClass).filter(RDFClass.name == class_name).one()

    resource = Instance(id=object_["id"], name=object_["name"], type_=class_.id)
    session.add(resource)
    session.commit()

    for prop in object_["object"]:
        if prop != "category":
            try:
                property_ = session.query(Property).filter(Property.name == prop).one()
            except:
                pdb.set_trace()
            value = Terminal(value=object_["object"][prop], unit="number")
            session.add(value)
            session.commit()

            triple = Graph(
                subject=resource.id,
                subject_type="INSTANCE",
                abs_predicate=property_.id,
                object_id=value.id,
                object_type="TERMINAL"
            )
            triple_store.append(triple)

# Adding the objects and properties to the graph
session.add_all(triple_store)
session.commit()
