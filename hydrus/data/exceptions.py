"""Exceptions for the crud operations."""


class ClassNotFound(Exception):
    """Error when the RDFClass is not found."""

    def __init__(self, type_):
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self):
        """Return the HTTP response for the Exception."""
        return 400, {"message": "The class %s is not a valid/defined RDFClass" % self.type_}


class InstanceNotFound(Exception):
    """Error when the Instance is not found."""

    def __init__(self, id_):
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self):
        """Return the HTTP response for the Exception."""
        return 404, {"message": "Instance with ID %s not found" % self.id_}


class PropertyNotFound(Exception):
    """Error when the Property is not found."""

    def __init__(self, type_):
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self):
        """Return the HTTP response for the Exception."""
        return 400, {"message": "The property %s is not a valid/defined Property" % self.type_}


class InstanceExists(Exception):
    """Error when the Instance already exists."""

    def __init__(self, id_):
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self):
        """Return the HTTP response for the Exception."""
        return 400, {"message": "Instance with ID %s already exists" % self.id_}


class InstanceNotValid(Exception):
    """Error when the Instance is not valid."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        Exception.__init__(self, *args, **kwargs)

#
# class InstanceNotFound(Exception):
#     """Error when the Instance is not found."""
#
#     def __init__(self, *args, **kwargs):
#         """Constructor."""
#         Exception.__init__(self, *args, **kwargs)
