from cauth.configuration import Variable


def test_domain() -> None:
    assert Variable(name="foo", values={"domain": {"name": "bar"}}).domain.name == "bar"


def test_name() -> None:
    assert Variable(name="foo", values={}).name == "foo"
