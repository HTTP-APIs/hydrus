"""Definition of all Classes in the SubSystem vocabulary."""

import models
from sqlalchemy.orm import sessionmaker


classes = {
    "Spacecraft_Communication": models.Classes(name="Spacecraft_Communication"),
    "Spacecraft_Propulsion": models.Classes(name="Spacecraft_Propulsion"),
    "Spacecraft_Detector": models.Classes(name="Spacecraft_Detector"),
    "Spacecraft_PrimaryPower": models.Classes(name="Spacecraft_PrimaryPower"),
    "Spacecraft_Thermal": models.Classes(name="Spacecraft_Thermal"),
    "Spacecraft_Structure": models.Classes(name="Spacecraft_Structure"),
    "Spacecraft_CDH": models.Classes(name="Spacecraft_CDH"),
    "Spacecraft_AODCS": models.Classes(name="Spacecraft_AODCS"),
}

if __name__ == "__main__":
    Session = sessionmaker(bind=models.engine)
    session = Session()

    session.add_all([classes[x] for x in classes])
    session.commit()
