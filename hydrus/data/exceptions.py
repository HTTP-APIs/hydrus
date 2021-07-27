"""Exceptions for the crud operations."""
from typing import Dict, Tuple, Union, Any, List
from hydra_python_core.doc_writer import HydraError


class ClassNotFound(Exception):
    """Error when the RDFClass is not found."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"The class {self.type_} is not a valid/defined RDFClass"
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
            description = f"Instance of type {self.type_} not found"
            return HydraError(code=404, title="Instance not found", desc=description)
        else:
            description = (
                f"Instance of type {self.type_} with ID {str(self.id_)} not found"
            )
            return HydraError(code=404, title="Instance not found", desc=description)


class MemberInstanceNotFound(Exception):
    """Error when the Instance (Member in Collection) is not found."""

    def __init__(
        self,
        type_: str,
        collection_id_: Union[str, None]=None,
        member_id_: Union[str, None]=None,
    ) -> None:
        """Constructor."""
        self.type_ = type_
        self.collection_id = collection_id_
        self.member_id = member_id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        if str(self.member_id) is None:
            description = f"Instance of type {self.type_} not found"
            return HydraError(code=404, title="Instance not found", desc=description)
        else:
            description = (
                f"Instance of type {self.type_} with"
                f" Collection ID {str(self.collection_id)}"
                f" and member_id {str(self.member_id)} not found"
            )
            return HydraError(code=404, title="Instance not found", desc=description)


class PropertyNotFound(Exception):
    """Error when the Property is not found."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"The property {self.type_} is not a valid/defined Property"
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
            description = f"Instance of type {self.type_} already exists"
            return HydraError(
                code=400, title="Instance already exists.", desc=description
            )
        else:
            description = (
                f"Instance of type {self.type_} with ID {str(self.id_)} already exists"
            )
            return HydraError(
                code=400, title="Instance already exists.", desc=description
            )


class UserExists(Exception):
    """Error when the User already exitst."""

    def __init__(self, id_: int) -> None:
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"The user with ID {self.id_} already exists"
        return HydraError(code=400, title="User already exists.", desc=description)


class UserNotFound(Exception):
    """Error when the User is not found."""

    def __init__(self, id_: int) -> None:
        """Constructor."""
        self.id_ = id_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"The User with ID {self.id_} is not a valid/defined User"
        return HydraError(code=400, title="User not found", desc=description)


class PageNotFound(Exception):
    """Error when the page is not found."""

    def __init__(self, page_id: str) -> None:
        """Constructor."""
        self.page_id = page_id

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"The page with ID {self.page_id} not found"
        return HydraError(code=400, title="Page not found", desc=description)


class InvalidSearchParameter(Exception):
    "Error when client uses invalid query parameter for searching."

    def __init__(self, param: str) -> None:
        """Constructor."""
        self.param = param

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"Query parameter [{self.param}] is invalid"
        return HydraError(code=400, title="Invalid query parameter", desc=description)


class IncompatibleParameters(Exception):
    """Error when two or more query parameters are incompatible with each other."""

    def __init__(self, params: List[str]) -> None:
        """Constructor."""
        self.params = params

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = "Following parameters are incompatible with each other: ["
        for i in range(len(self.params)):
            if i == len(self.params) - 1:
                description += f"{self.params[i]}]"
            else:
                description += f"{self.params[i]}, "
        return HydraError(code=400, title="Incompatible parameters.", desc=description)


class OffsetOutOfRange(Exception):
    """Error when the offset provided by client is out of range"""

    def __init__(self, offset: str) -> None:
        """Constructor."""
        self.offset = offset

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"Offset {self.offset} is out of range."
        return HydraError(code=400, title="Page not found", desc=description)


class PropertyNotGiven(Exception):
    """Error when a Property is not given."""

    def __init__(self, type_: str) -> None:
        """Constructor."""
        self.type_ = type_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = f"The property {self.type_} is not given."
        return HydraError(code=400, title="Property not given", desc=description)


class InvalidDateTimeFormat(Exception):
    """Error when a datetime field input is invalid"""

    def __init__(self, field_: str) -> None:
        """Constructor."""
        self.field_ = field_

    def get_HTTP(self) -> HydraError:
        """Return the HTTP response for the Exception."""
        description = (f"The format of {self.field_} is invalid."
                       f" Datetime input should be in ISO format.")
        return HydraError(code=400, title="Invalid Datetime format", desc=description)
