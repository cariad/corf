from typing import Optional

from pytest import mark

from corf.configuration import Domain


@mark.parametrize(
    "values, expect",
    [
        ({}, None),
        ({"account": "000000000000"}, "000000000000"),
    ],
)
def test_account(values: dict, expect: Optional[str]) -> None:
    assert Domain(values).account == expect


@mark.parametrize(
    "values, expect",
    [
        ({"name": "foo"}, "foo"),
    ],
)
def test_name(values: dict, expect: Optional[str]) -> None:
    assert Domain(values).name == expect


@mark.parametrize(
    "values, expect",
    [
        ({}, None),
        ({"region": "foo"}, "foo"),
    ],
)
def test_region(values: dict, expect: Optional[str]) -> None:
    assert Domain(values).region == expect


@mark.parametrize(
    "values, expect",
    [
        ({}, None),
        ({"profile": "foo"}, "foo"),
    ],
)
def test_profile(values: dict, expect: Optional[str]) -> None:
    assert Domain(values).profile == expect
