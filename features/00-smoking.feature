@smoking-status
Feature: Smoking status

    @DSTU2 @STU3
    Scenario: Correct resourceType
        Given I have a Smoking status response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Smoking status response
        Then the resource parses as valid FHIR DSTU2 content

    @STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Smoking status response
        Then the resource parses as valid FHIR STU3 content

    @DSTU2 @STU3
    Scenario: Results exist
        Given I have a Smoking status response
        Then there should be at least 1 Observation entry

    @DSTU2 @STU3
    Scenario: Resources have ids
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then all resources will have a id field

    @DSTU2 @STU3
    Scenario: All references will resolve
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then all references will resolve

    @DSTU2 @STU3
    Scenario: All the codes are valid
        Given I have a Smoking status response
        And there is at least 1 Observation entry
        Then all the codes will be valid

    @warning @DSTU2 @STU3
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
