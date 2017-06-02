"""Definition of all Classes in the SubSystem and Spacecraft vocabulary."""

import models
from sqlalchemy.orm import sessionmaker

# TODO @xadahiya:
# Refactor this part to use a JSON-LD parser, so that RDF classes
#  can be directly imported from the vocabulary. Add the classes in the
#  `spacecraft` vocabulary.
classes = {
    "Spacecraft_Communication": models.Classes(name="Spacecraft_Communication"),
    "Spacecraft_Propulsion": models.Classes(name="Spacecraft_Propulsion"),
    "Spacecraft_Detector": models.Classes(name="Spacecraft_Detector"),
    "Spacecraft_PrimaryPower": models.Classes(name="Spacecraft_PrimaryPower"),
    "Spacecraft_BackupPower": models.Classes(name="Spacecraft_BackupPower"),
    "Spacecraft_Thermal": models.Classes(name="Spacecraft_Thermal"),
    "Spacecraft_Structure": models.Classes(name="Spacecraft_Structure"),
    "Spacecraft_CDH": models.Classes(name="Spacecraft_CDH"),
    "Spacecraft_AODCS": models.Classes(name="Spacecraft_AODCS"),
    "Spacecraft": models.Classes(name="Spacecraft"),
    "Subsystem_Spacecraft": models.Classes(name="Subsystem_Spacecraft"),  # all the subsystems types, except detectors (or experiments)
    "Payload_Spacecraft": models.Classes(name="Payload_Spacecraft")  # Detectors are payload not strictly subssytems
}

if __name__ == "__main__":
    Session = sessionmaker(bind=models.engine)
    session = Session()

    session.add_all([classes[x] for x in classes])
    session.commit()
