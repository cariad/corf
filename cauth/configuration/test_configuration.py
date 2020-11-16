from os import chdir
from pathlib import Path
from typing import List

from cauth.configuration import Configuration, Variable

testing_dir = Path(__file__).parent.parent.parent.joinpath("testing")
test_project_dir = testing_dir.joinpath("sample_filesystem").joinpath("project-foo")


def test_configuration_directories() -> None:
    # Build our own list of expected directories.
    expect_directories: List[Path] = []
    expect_directories.append(Path.home().absolute())
    for path in reversed(Path().absolute().parents):
        expect_directories.append(path.absolute())
    expect_directories.append(Path().absolute())

    # Assert that all the yielded directories are correct.
    actuals = Configuration().get_configuration_directories()
    for expect in expect_directories:
        assert next(actuals, None) == expect

    # Assert that no more directories are yielded.
    assert next(actuals, None) is None


def test_get_variables() -> None:
    chdir(test_project_dir)

    # The user running the tests could have their own configuration files in the search
    # paths, so we shouldn't assert that we find *only* our test configurations.
    expect = ["VAR_1", "VAR_2"]
    actuals = Configuration().load().get_variables()

    while var := next(actuals, None):
        if var.name in expect:
            expect.remove(var.name)
        assert_variable(var=var, fail_on_unexpected=False)

    # Assert that we found everything that we expected to.
    assert len(expect) == 0


def assert_variable(var: Variable, fail_on_unexpected: bool) -> None:
    if var.name == "VAR_1":
        assert var.domain.account == "team-account-for-project-v1"
        assert var.domain.name == "user-domain-for-project-v1"
        assert var.domain.region == "team-region-for-global-v1"
        assert var.domain.profile == "user-profile-for-project-v1"
    elif var.name == "VAR_2":
        assert var.domain.account == "team-account-for-global-v2"
        assert var.domain.name == "team-domain-for-project-v2"
        assert var.domain.region == "team-region-for-global-v2"
        assert var.domain.profile == "user-profile-for-global-v2"
    else:
        assert not fail_on_unexpected
