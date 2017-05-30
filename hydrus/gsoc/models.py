"""Models for Hydra Classes."""


class Property:
    """Class for Hydra Property.

    >>> prop1 = Property('maxWorkingTemperature')
    >>> prop2 = Property('minWorkingTemperature')
    """

    def __init__(self, name):
        """Constructor."""
        self.name = name


class SubSysType:
    """Generic class for Hydra SubSystem.

    >>> primary_power = SubSysType('Spacecraft_PrimaryPower', [ prop1, prop2, ...])
    >>> backup_power = SubSysType('Spacecraft_BackupPower', [ prop1, prop2, ...])
    """

    def __init__(self, type_, allowed_properties):
        """Constructor."""
        self.type_ = type_
        self.allowed_properties = allowed_properties


class Resource:
    """Generic Resource class for Hydra objects.

    >>> component1 = Resource(name=123, type=primary_power, [...])
    >>> component2 = Resource(name=123, type=backup_power, [...])
    """

    def __init__(self, id_, name, type_):
        """Constructor."""
        self.id = id_
        self.name = name
        self.type = type_


class Graph:
    """Graph triple contains subject, predicate, object.

    >>> Graph(component1, attribute, component2)
    """

    def __init__(self, subject, predicate, object_):
        """Constructor."""
        self.subject = subject
        self.predicate = predicate
        self.object = object_

    def hydrafy(self):
        """Generate Hydra compatible JSON for the instance."""
        pass
