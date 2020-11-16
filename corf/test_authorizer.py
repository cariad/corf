from typing import Optional

from mock import Mock, patch
from pytest import mark

from corf.authoriser import Authoriser
from corf.configuration import Domain


@mark.parametrize(
    "values, expect",
    [
        ({}, {}),
        ({"region": "eu-west-2"}, {"region_name": "eu-west-2"}),
    ],
)
def test_client_kwargs(values: dict, expect: dict) -> None:
    kwargs = Authoriser(domain=Domain(values)).client_kwargs
    # kwargs["config"] is a boto object that we can't easily describe in our
    # expectations above. We'll test it "menually" here, then remove it from the
    # response before asserting it matches our expectation.
    assert kwargs["config"].connect_timeout == 3
    assert kwargs["config"].read_timeout == 20
    assert kwargs["config"].retries == {"max_attempts": 20}
    del kwargs["config"]
    assert kwargs == expect


@patch("corf.authoriser.Session")
def test_get_token(session_maker: Mock) -> None:
    session = Mock()
    session_maker.return_value = session

    client = Mock()
    client.get_authorization_token.return_value = {"authorizationToken": "foo"}
    session.client.return_value = client

    assert Authoriser(domain=Domain({"name": "mydomain"})).get_token() == "foo"


@mark.parametrize(
    "values, profile, expect",
    [
        ({}, None, {}),
        ({}, "foo", {"profile_name": "foo"}),
        ({"profile": "foo"}, None, {"profile_name": "foo"}),
        ({"profile": "foo"}, "bar", {"profile_name": "bar"}),
    ],
)
def test_session_kwargs(values: dict, profile: Optional[str], expect: dict) -> None:
    assert Authoriser(domain=Domain(values), profile=profile).session_kwargs == expect


@mark.parametrize(
    "values, expect",
    [
        ({"name": "foo"}, {"domain": "foo"}),
        (
            {"name": "foo", "account": "000000000000"},
            {"domain": "foo", "domainOwner": "000000000000"},
        ),
    ],
)
def test_token_kwargs(values: dict, expect: dict) -> None:
    assert Authoriser(domain=Domain(values)).token_kwargs == expect
