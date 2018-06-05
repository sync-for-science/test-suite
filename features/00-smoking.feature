@use.with_use_case=ehr @smoking-status
Feature: Smoking status

    Scenario: Correct URI
        Given I have a Smoking status response
        Then the correct URI was used

    Scenario: Correct resourceType
        Given I have a Smoking status response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @use.with_version=DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Smoking status response
        Then the resource parses as valid FHIR DSTU2 content

    @use.with_version=STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Smoking status response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Results exist
        Given I have a Smoking status response
        Then there should be at least 1 Observation entry

    Scenario: Resources have ids
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Smoking Status profile
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then there exists one status in Observation.status
        Then Observation.status is bound to http://hl7.org/fhir/observation-status
        Then there exists one code in Observation.code
        Then there exists a fixed Observation.code.coding.system=http://loinc.org
        Then there exists a fixed Observation.code.coding.code=72166-2
        Then there exists one reference to a Patient in Observation.subject
        Then there exists one instant in Observation.issued
        Then there exists one value in Observation.valueCodeableConcept
        Then Observation.valueCodeableConcept is bound to http://hl7.org/fhir/ValueSet/daf-observation-ccdasmokingstatus
