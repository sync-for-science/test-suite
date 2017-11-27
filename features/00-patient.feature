@use.with_use_case=ehr @patient-demographics
Feature: Patient demographics

    Scenario: Correct resourceType
        Given I have a Patient demographics response
        Then the resourceType field will be Patient

    @use.with_version=DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Patient demographics response
        Then the resource parses as valid FHIR DSTU2 content

    @use.with_version=STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Patient demographics response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Patients have ids
        Given I have a Patient demographics response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Patient demographics response
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Patient demographics response
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Patient profile
        Given I have a Patient demographics response
        Then there exists one or more medical record numbers in Patient.identifier
        And each Patient.identifier must have a identifier.system
        And each Patient.identifier must have a identifier.value
        Then there exists one or more names in Patient.name
        And each Patient.name must have a name.family
        And each Patient.name must have a name.given
        Then there exists one administrative gender in Patient.gender
