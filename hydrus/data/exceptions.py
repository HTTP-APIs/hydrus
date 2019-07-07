"""Exceptions for the crud operations."""
from typing import Dict, Tuple, Union, Any
from hydra_python_core.doc_writer import HydraError


class ClassNotFound(Exception):
    """Error when the RDFClass is not found."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The class {} is not a valid/defined RDFClass".format(self.type_)
        return HydraError(code=400, title="Invalid class", desc=description)


class InstanceNotFound(Exception):
    """Error when the Instance is not found."""

    def __init__(self, type_: str, id_: Union[str, None]=None) -> None:
        """Constructor."""
        self.type_ = type_
        self.id_ = id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        if str(self.id_) is None:
            description = "Instance of type {} not found".format(self.type_)
            return HydraError(code=404, title="Instance not found", desc=description)
        else:
            description = "Instance of type {} with ID {} not found".format(
                self.type_, str(self.id_))
            return HydraError(code=404, title="Instance not found", desc=description)


class PropertyNotFound(Exception):
    """Error when the Property is not found."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The property {} is not a valid/defined Property".format(self.type_)
        return HydraError(code=400, title="Property not found", desc=description)


class InstanceExists(Exception):
    """Error when the Instance already exists."""

    def __init__(self, type_: str, id_: Union[str, None]=None) -> None:
        """Constructor."""
        self.type_ = type_
        self.id_ = id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        if str(self.id_) is None:
            description = "Instance of type {} already exists".format(self.type_)
            return HydraError(code=400, title="Instance already exists.", desc=description)
        else:
            description = "Instance of type {} with ID {} already exists".format(
                self.type_, str(self.id_))
            return HydraError(code=400, title="Instance already exists.", desc=description)


class NotInstanceProperty(Exception):
    """Error when the property is not an Instance property."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The property {} is not an Instance property".format(self.type_)
        return HydraError(code=400, title="Not an Instance property", desc=description)


class NotAbstractProperty(Exception):
    """Error when the property is not an Abstract property."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The property {} is not an Abstract property".format(self.type_)
        return HydraError(code=400, title="Not an Abstract property", desc=description)


class UserExists(Exception):
    """Error when the User already exitst."""

    def __init__(self, id_: int) -> None:
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The user with ID {} already exists".format(self.id_)
        return HydraError(code=400, title="User already exists.", desc=description)


class UserNotFound(Exception):
    """Error when the User is not found."""

    def __init__(self, id_: int) -> None:
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The User with ID {} is not a valid/defined User".format(self.id_)
        return HydraError(code=400, title="User not found", desc=description)


class PageNotFound(Exception):
    """Error when the User is not found."""

    def __init__(self, page_id: str) -> None:
        """Constructor."""
        self.page_id = page_id

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "The page with ID {} not found".format(self.page_id)
        return HydraError(code=400, title="Page not found", desc=description)


class InvalidSearchParameter(Exception):
    "Error when client uses invalid query parameter for searching."

    def __init__(self, param: str) -> None:
        """Constructor."""
        self.param = param

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "Query parameter [{}] is invalid".format(self.param)
        return HydraError(code=400, title="Invalid query parameter", desc=description)
