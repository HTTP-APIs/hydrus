"""Definition of all Properties in the SubSystem vocabulary."""

from models import Property, engine
from sqlalchemy.orm import sessionmaker

abstract_properties = {
    "hasWireInWith": Property(name="hasWireInWith", type_="ABSTRACT"),
    "hasWireOutWith": Property(name="hasWireOutWith", type_="ABSTRACT"),
    "manufacturer": Property(name="manufacturer", type_="ABSTRACT"),
    "function": Property(name="function", type_="ABSTRACT"),
    "subSystemType": Property(name="subSystemType", type_="ABSTRACT"),
    "isStandard": Property(name="isStandard", type_="ABSTRACT"),
    "holdsSensor": Property(name="holdsSensor", type_="ABSTRACT"),
    "typeOfPropellant": Property(name="typeOfPropellant", type_="ABSTRACT"),
}

instance_properties = {
    "minWorkingTemperature": Property(name="minWorkingTemperature", type_="INSTANCE"),
    "maxWorkingTemperature": Property(name="maxWorkingTemperature", type_="INSTANCE"),
    "minTemperature": Property(name="minTemperature", type_="INSTANCE"),
    "maxTemperature": Property(name="maxTemperature", type_="INSTANCE"),
    "hasVolume": Property(name="hasVolume", type_="INSTANCE"),
    "hasMinAmpere": Property(name="hasMinAmpere", type_="INSTANCE"),
    "hasMaxAmpere": Property(name="hasMaxAmpere", type_="INSTANCE"),
    "hasMass": Property(name="hasMass", type_="INSTANCE"),
    "hasMonetaryValue": Property(name="hasMonetaryValue", type_="INSTANCE"),
    "hasPower": Property(name="hasPower", type_="INSTANCE"),
    "hasSpecificImpulse": Property(name="hasSpecificImpulse", type_="INSTANCE"),
    "type": Property(name="type", type_="INSTANCE"),
    "mechanism": Property(name="mechanism", type_="INSTANCE"),
}

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([abstract_properties[x] for x in abstract_properties])
    session.commit()

    session.add_all(instance_properties[x] for x in instance_properties)
    session.commit()
