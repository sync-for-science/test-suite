from features.steps.deciders import ArgonautObservationDecider
from tests.testvitals import VitalsResource
from features.steps.argonaut import found_at_least_one


def test_argonaut_validation():
    resources = VitalsResource().get_resources()

    assert ArgonautObservationDecider(resources[0]).should_validate()
    assert not ArgonautObservationDecider(resources[1]).should_validate()


def test_found_one():
    resources = VitalsResource().get_resources()

    resource_path = "Observation.category.coding.code".split(".")
    resource_path.pop(0)

    fake_resource = resources[0]

    assert found_at_least_one([fake_resource], resource_path, "vital-signs")

    fake_resource["category"]["coding"][0]["code"] = "not-vital-signs"

    assert not found_at_least_one([fake_resource], resource_path, "vital-signs")
