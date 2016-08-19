@smoking-status
Feature: Smoking status

    Scenario: Correct resourceType
        Given I have a Smoking status response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Smoking status response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Smoking status response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Smoking status response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Smoking status response
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Smoking status response
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Smoking Status profile
        Given I have a Smoking status response
        Then there exists one status in Observation.status
        Then Observation.status is bound to http://hl7.org/fhir/observation-status
        Then there exists one code in Observation.code
        Then there exists a fixed Observation.code.coding.system=http://loinc.org
        Then there exists a fixed Observation.code.coding.code=72166-2
        Then there exists one reference to a Patient in Observation.subject
        Then there exists one instant in Observation.issued
        Then there exists one value in Observation.valueCodeableConcept
        Then Observation.valueCodeableConcept.coding.code is bound to http://hl7.org/fhir/ValueSet/daf-observation-ccdasmokingstatus
