from copy import deepcopy
from pathlib import Path
from typing import Generator

from yaml import safe_load

from corf.configuration import Variable


class Configuration(dict):
    def get_configuration_directories(self) -> Generator[Path, None, None]:
        """
        Yields the directories from which to load configuration files.
        """
        # The lowest-priority is the user's home directory.
        yield Path.home().absolute()
        # The configuration can be overwritten by directories of increasing priority
        # as we approach the working directory.
        for path in reversed(Path().absolute().parents):
            yield path.absolute()
        # Finally, the directory with the highest priority is the working directory.
        yield Path().absolute()

    def get_variables(self) -> Generator[Variable, None, None]:
        """
        Yields all the `EnvironmentVariable` to apply.
        """
        for name in self["variables"]:
            yield Variable(name=name, values=self["variables"][name])

    def load(self) -> "Configuration":
        """
        Loads and merges all available configuration files.
        """
        for directory in self.get_configuration_directories():
            for filename in [".corf.yml", ".corf.user.yml"]:
                path = directory.joinpath(filename)
                try:
                    with open(path, "r") as stream:
                        self.merge(source=safe_load(stream), destination=self)
                        print("corf merged configuration:", path)
                except FileNotFoundError:
                    pass
        return self

    def merge(self, source: dict, destination: dict) -> None:
        """
        Merges two dictionaries.
        """
        for key in source:
            if key not in destination or not isinstance(source[key], dict):
                destination[key] = deepcopy(source[key])
            else:
                self.merge(source[key], destination[key])
