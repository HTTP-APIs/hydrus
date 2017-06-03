"""Definition of all Classes in the SubSystem and Spacecraft vocabulary."""

import models
from sqlalchemy.orm import sessionmaker
from spacecraft_jsonld import spacecraft_data
from subsystem_jsonld import subsystem_data



def filter_objects(data, key='@type', value='http://www.w3.org/2002/07/owl#Class'):
    """ Return a filtered list of objects provided given key, value pair and data. """
    obj_list = []
    for obj in data['defines']:
        if key in obj.keys():
            if obj[key] == value:
                obj_list.append(obj)
    return obj_list


def get_rdf_lables(obj_list):
    """ Get rdf:labels from a given list of objects. """
    rdf_labels = []
    for obj in obj_list:
        rdf_labels.append(obj['rdf:label'])

    return rdf_labels



def gen_classes(labels):
    """ Generate sqlalchemy Classes model (from models.py) instances for a given set of labels"""
    classes = []
    for label in labels:
        classes.append(models.RDFClass(name=label))
    return classes


# Generate classes for subsystem data
subsystem_labels = get_rdf_lables(filter_objects(subsystem_data))
subsystem_classes = gen_classes(subsystem_labels)

# Generate classes for the spacecraft data
spacecraft_labels = get_rdf_lables(filter_objects(spacecraft_data))
spacecraft_classes = gen_classes(spacecraft_labels)


# classes = {
#     "Spacecraft_Communication": models.Classes(name="Spacecraft_Communication"),
#     "Spacecraft_Propulsion": models.Classes(name="Spacecraft_Propulsion"),
#     "Spacecraft_Detector": models.Classes(name="Spacecraft_Detector"),
#     "Spacecraft_PrimaryPower": models.Classes(name="Spacecraft_PrimaryPower"),
#     "Spacecraft_BackupPower": models.Classes(name="Spacecraft_BackupPower"),
#     "Spacecraft_Thermal": models.Classes(name="Spacecraft_Thermal"),
#     "Spacecraft_Structure": models.Classes(name="Spacecraft_Structure"),
#     "Spacecraft_CDH": models.Classes(name="Spacecraft_CDH"),
#     "Spacecraft_AODCS": models.Classes(name="Spacecraft_AODCS"),
#     "Spacecraft": models.Classes(name="Spacecraft"),
#     "Subsystem_Spacecraft": models.Classes(name="Subsystem_Spacecraft"),  # all the subsystems types, except detectors (or experiments)
#     "Payload_Spacecraft": models.Classes(name="Payload_Spacecraft")  # Detectors are payload not strictly subssytems
# }
#
if __name__ == "__main__":
    Session = sessionmaker(bind=models.engine)
    session = Session()

    session.add_all(subsystem_classes)
    session.commit()
    print("Subsystem classes added successfully")

    session.add_all(spacecraft_classes)
    session.commit()
    print("Spacecraft classes added succesfully")
