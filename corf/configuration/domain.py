from typing import Dict, Optional


class Domain(dict):
    """
    Represents the configuration for an AWS CodeArtifact domain.

    Arguments:
        values (dict): Configuration values.
    """

    def __init__(self, values: Dict[str, str]):
        self.update(values)

    @property
    def account(self) -> Optional[str]:
        return self.get("account", None)

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def region(self) -> Optional[str]:
        return self.get("region", None)

    @property
    def profile(self) -> Optional[str]:
        return self.get("profile", None)
