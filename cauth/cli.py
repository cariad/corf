from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import getLogger
from typing import List, Optional

from cauth.configuration import Configuration
from cauth.executor import Executor
from cauth.version import get_version


class CLI:
    """
    CLI executor.

    Arguments:
        args (List[str]): Optional arguments. Will read from the command line if
                          omitted. Intended for tests.
    """

    def __init__(self, args: Optional[List[str]] = None) -> None:
        self.cli_args = args
        self.parsed_args: Optional[Namespace] = None

    @property
    def args(self) -> Namespace:
        """
        Gets the commandline arguments.
        """
        self.parsed_args = self.parsed_args or self.make_arg_parser().parse_args(
            self.cli_args
        )
        return self.parsed_args

    def execute(self) -> int:
        """
        Execute the prescribed shell command with environment variables populated with
        AWS CodeArtifact domain authorization tokens.

        Returns:
            int: Shell return code.
        """
        try:
            return Executor(
                command=self.args.command,
                config=Configuration().load(),
                profile=self.args.profile,
            ).execute()
        except Exception as e:
            print(f"cauth failed: {str(e)}")
            return 1

    def invoke(self) -> int:
        """
        Invokes the apppriate task for the given command line arguments.

        Returns:
            int: Shell return code.
        """
        self.setup_logging()

        if self.args.info:
            return self.print_info()

        if self.args.version:
            return self.print_version()

        if self.args.command:
            return self.execute()

        return self.print_help()

    def make_arg_parser(self) -> ArgumentParser:
        """
        Gets an `ArgumentParser` populated for CLI usage.
        """
        ap = ArgumentParser(
            "cauth",
            description="""
"cauth" is an AWS CodeArtifact authorization helper for "pipenv" and other command line
tools that read CodeArtifact authorization tokens.

See https://github.com/cariad/cauth for full instructions.""",
            epilog="""
examples:
# To run "pipenv install --dev" with an AWS CodeArtifact authorization token set:
cauth pipenv install --dev

# To use a specific AWS named profile:
cauth --profile corp pipenv install --dev

# To run any command with an AWS CodeArtifact authorization token set:
cauth COMMAND""",
            formatter_class=RawDescriptionHelpFormatter,
            usage="cauth [OPTIONS] COMMAND",
        )
        ap.add_argument("--info", action="store_true", help="prints information")
        ap.add_argument("--profile", help="named AWS profile to use for authentication")
        ap.add_argument("--version", action="store_true", help="print the version")
        ap.add_argument("command", nargs="...")
        return ap

    def print_help(self) -> int:
        """
        Prints help.

        Returns:
            int: Shell return code.
        """
        self.make_arg_parser().print_help()
        return 0

    def print_info(self) -> int:
        """
        Prints information.

        Returns:
            int: Shell return code.
        """
        print(get_version())
        print(Configuration().load())
        return 0

    def print_version(self) -> int:
        """
        Prints the version.

        Returns:
            int: Shell return code.
        """
        print(get_version())
        return 0

    def setup_logging(self) -> None:
        """
        Sets up logging.
        """
        # We don't log anything ourselves, but we do want to quieten boto for a pleasant
        # console experience.
        getLogger("boto").setLevel("CRITICAL")
