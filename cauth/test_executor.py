from os import environ
from typing import Optional

from mock import Mock, call, patch
from pytest import mark

from cauth.configuration import Configuration, Variable
from cauth.executor import Executor


@mark.parametrize("profile", [(None), ("foo")])
@patch("cauth.executor.Authorizer")
def test_make_variables(authorizer_maker: Mock, profile: Optional[str]) -> None:
    environ["CAUTH_UNITTEST"] = "1"

    authorizer_1 = Mock()
    authorizer_1.get_token.return_value = "token-1"

    authorizer_2 = Mock()
    authorizer_2.get_token.return_value = "token-2"

    authorizer_maker.side_effect = [authorizer_1, authorizer_2]

    configuration = Mock()
    var_1 = Variable(name="VAR_1", values={"domain": {"name": "domain-1"}})
    var_2 = Variable(name="VAR_2", values={"domain": {"name": "domain-2"}})

    configuration.get_variables.return_value = iter([var_1, var_2])

    executor = Executor(
        command=["pipenv", "sync"],
        config=configuration,
        profile=profile,
    )

    actuals = executor.make_variables()
    del environ["CAUTH_UNITTEST"]

    # Assert that our tokens are set.
    assert actuals["VAR_1"] == "token-1"
    assert actuals["VAR_2"] == "token-2"

    # Assert that all current environment variables are included.
    assert actuals["CAUTH_UNITTEST"] == "1"

    assert authorizer_maker.call_count == 2
    authorizer_maker.assert_has_calls([call(domain=var_1.domain, profile=profile)])
    authorizer_maker.assert_has_calls([call(domain=var_2.domain, profile=profile)])


@patch("cauth.executor.Executor.make_variables")
@patch("cauth.executor.run")
def test_execute(run: Mock, make_variables: Mock) -> None:
    make_variables.return_value = {"token": "foo"}
    executor = Executor(
        command=["pipenv", "sync"],
        config=Configuration(),
    )
    run_response = Mock()
    run_response.returncode = 1
    run.return_value = run_response
    assert executor.execute() == 1
    run.assert_called_with(["pipenv", "sync"], env={"token": "foo"})
