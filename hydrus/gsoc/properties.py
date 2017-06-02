"""Definition of all Properties in the SubSystem vocabulary."""

from models import Property, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

abstract_properties = [
    Property(name="hasWireInWith", type_="ABSTRACT"),
    Property(name="hasWireOutWith", type_="ABSTRACT"),
    Property(name="manufacturer", type_="ABSTRACT"),
    Property(name="function", type_="ABSTRACT"),
    Property(name="subSystemType", type_="ABSTRACT"),
    Property(name="isStandard", type_="ABSTRACT"),
    Property(name="holdsSensor", type_="ABSTRACT"),
    Property(name="typeOfPropellant", type_="ABSTRACT"),
]

instance_properties = [
    Property(name="minWorkingTemperature", type_="INSTANCE"),
    Property(name="maxWorkingTemperature", type_="INSTANCE"),
    Property(name="hasVolume", type_="INSTANCE"),
    Property(name="hasMinAmpere", type_="INSTANCE"),
    Property(name="hasMaxAmpere", type_="INSTANCE"),
    Property(name="hasMass", type_="INSTANCE"),
    Property(name="hasMonetaryValue", type_="INSTANCE"),
    Property(name="hasMonetaryValue", type_="INSTANCE"),
    Property(name="hasPower", type_="INSTANCE"),
    Property(name="hasSpecificImpulse", type_="INSTANCE"),
]

session.add_all(abstract_properties)
session.commit()

session.add_all(instance_properties)
session.commit()
