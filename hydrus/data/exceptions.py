"""Exceptions for the crud operations."""
from typing import Dict, Tuple, Union


class ClassNotFound(Exception):
    """Error when the RDFClass is not found."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        return 400, {
            "message": "The class {} is not a valid/defined RDFClass".format(self.type_)}


class InstanceNotFound(Exception):
    """Error when the Instance is not found."""

    def __init__(self, type_: str, id_: Union[str, None]=None) -> None:
        """Constructor."""
        self.type_ = type_
        self.id_ = id_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        if str(self.id_) is None:
            return 404, {
                "message": "Instance of type {} not found".format(self.type_)}
        else:
            return 404, {"message": "Instance of type {} with ID {} not found".format(
                self.type_, str(self.id_))}


class PropertyNotFound(Exception):
    """Error when the Property is not found."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        return 400, {
            "message": "The property {} is not a valid/defined Property".format(self.type_)}


class InstanceExists(Exception):
    """Error when the Instance already exists."""

    def __init__(self, type_: str, id_: Union[str, None]=None) -> None:
        """Constructor."""
        self.type_ = type_
        self.id_ = id_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        if str(self.id_) is None:
            return 400, {
                "message": "Instance of type {} already exists".format(self.type_)}
        else:
            return 400, {"message": "Instance of type {} with ID {} already exists".format(
                self.type_, str(self.id_))}


class NotInstanceProperty(Exception):
    """Error when the property is not an Instance property."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        return 400, {
            "message": "The property {} is not an Instance property".format(self.type_)}


class NotAbstractProperty(Exception):
    """Error when the property is not an Abstract property."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        return 400, {
            "message": "The property {} is not an Abstract property".format(self.type_)}


class UserExists(Exception):
    """Error when the User already exitst."""

    def __init__(self, id_: int) -> None:
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        return 400, {
            "message": "The user with ID {} already exists".format(self.id_)}


class UserNotFound(Exception):
    """Error when the User is not found."""

    def __init__(self, id_: int) -> None:
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self) -> Tuple[int, Dict[str, str]]:
        """Return the HTTP response for the Exception."""
        return 400, {
            "message": "The User with ID {} is not a valid/defined User".format(self.id_)}
