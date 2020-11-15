from typing import Any, Dict

from cauth.configuration import Domain


class Variable(dict):
    """
    Represents the configuration for an environment variable.

    Arguments:
        name (str):    Environment variable name.
        values (dict): Configuration values.
    """

    def __init__(self, name: str, values: Dict[str, Any]):
        self.name = name
        self.update(values)

    @property
    def domain(self) -> Domain:
        return Domain(self["domain"])
