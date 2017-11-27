@use.with_use_case=ehr @medication-administrations
Feature: Medication administrations

    Scenario: Correct resourceType
        Given I have a Medication administrations response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @use.with_version=DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Medication administrations response
        Then the resource parses as valid FHIR DSTU2 content

    @use.with_version=STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Medication administrations response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Results exist
        Given I have a Medication administrations response
        Then there should be at least 1 MedicationAdministration entry

    Scenario: Resources have ids
        Given I have a Medication administrations response
        And there is at least 1 MedicationAdministration entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Medication administrations response
        And there is at least 1 MedicationAdministration entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Medication administrations response
        And there is at least 1 MedicationAdministration entry
        Then all the codes will be valid
