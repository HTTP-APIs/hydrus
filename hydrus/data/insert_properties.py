"""Don't need this anymore, properties are inserted on runtime depending upon type of subject and object."""

# """Definition of all Properties in the SubSystem and Spacecraft vocabulary."""
#
# from models import AbstractProperty, Property, engine
# from sqlalchemy.orm import sessionmaker
#
#
# # NOTE: "holdsSensor" is a property that targets classes in the `sensors` vocabulary
# abstract_properties = {
#     "hasWireInWith": AbstractProperty(name="hasWireInWith"),  # points to an instance of Subsystem_Spacecraft subclasses
#     "hasWireOutWith": AbstractProperty(name="hasWireOutWith"),  # as above ^
#     "function": AbstractProperty(name="function"), # should point to some kind of activity in DBPedia (not used for now)
#     "subSystemType": AbstractProperty(name="subSystemType"),  # points to a class of devices in
#     "holdsSensor": AbstractProperty(name="holdsSensor"),
#     "isComponentOf": AbstractProperty(name="isComponentOf"),  # links a subsytemtype class to the spacecraft class
#     "type": AbstractProperty(name="type"),  # type is a "built-in" JSON-LD property and it's always present
#     "mechanism": Property(name="mechanism"),  # this is used only for subsystems of type Spacecraft_Detector
# }
#
# instance_properties = {  # these are all properties from an instance to terminals or external resources
#     "manufacturer": Property(name="manufacturer"),
#     "isStandard": Property(name="isStandard"),
#     "typeOfPropellant": AbstractProperty(name="typeOfPropellant"),
#     "minWorkingTemperature": Property(name="minWorkingTemperature"),
#     "maxWorkingTemperature": Property(name="maxWorkingTemperature"),
#     "minTemperature": Property(name="minTemperature"),
#     "maxTemperature": Property(name="maxTemperature"),
#     "hasVolume": Property(name="hasVolume"),
#     "hasMinAmpere": Property(name="hasMinAmpere"),
#     "hasMaxAmpere": Property(name="hasMaxAmpere"),
#     "hasMass": Property(name="hasMass"),
#     "hasMonetaryValue": Property(name="hasMonetaryValue"),
#     "hasPower": Property(name="hasPower"),
#     "hasSpecificImpulse": Property(name="hasSpecificImpulse"),
#     "type": Property(name="type"),
# }
#
# if __name__ == "__main__":
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     session.add_all([abstract_properties[x] for x in abstract_properties])
#     session.commit()
#
#     session.add_all(instance_properties[x] for x in instance_properties)
#     session.commit()
