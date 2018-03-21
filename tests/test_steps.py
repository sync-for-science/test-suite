from features.steps.deciders import ResourceDecider
from tests.testvitals import VitalsResource


def test_argonaut_validation():
    resources = VitalsResource().get_resources()

    assert ResourceDecider(resources[0]).should_validate()
    assert not ResourceDecider(resources[1]).should_validate()



