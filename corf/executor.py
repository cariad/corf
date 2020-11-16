from os import environ
from subprocess import run
from typing import Dict, List, Optional

from corf.authoriser import Authoriser
from corf.configuration import Configuration


class Executor:
    """
    Shell command executor.

    Arguments:
        command (List[str]):    Command and arguments to execute.

        config (Configuration): Configuration.

        profile (str):          Optional AWS named profile to use during authorisation.
                                Will be used preferentially over any AWS named profile
                                described in any configuration files.
    """

    def __init__(
        self, command: List[str], config: Configuration, profile: Optional[str] = None
    ) -> None:
        self.command = command
        self.config = config
        self.profile = profile

    def make_variables(self) -> Dict[str, str]:
        """
        Gets the environment variables to set for the command.
        """
        variables = environ.copy()
        for var in self.config.get_variables():
            authoriser = Authoriser(domain=var.domain, profile=self.profile)
            print(f'Authorising "{var.name}"...')
            variables.update({var.name: authoriser.get_token()})
        return variables

    def execute(self) -> int:
        variables = self.make_variables()
        print(f'Starting "{self.command[0]}"...')
        return run(self.command, env=variables).returncode
