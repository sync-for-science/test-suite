@patient-demographics
Feature: Patient demographics

    Scenario: Correct resourceType
        Given I have a Patient demographics response
        Then the resourceType field will be Patient

    Scenario: Resources are valid FHIR content
        Given I have a Patient demographics response
        Then the resource parses as valid FHIR DSTU2 content

     Scenario: Patients have ids
        Given I have a Patient demographics response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Patient demographics response
        Then all references will resolve
