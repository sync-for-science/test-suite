Feature: requesting FHIR objects

    Scenario: Patients have IDs
        Given I am logged in
        When we request a Patient by id smart-1288992
        Then it will have an ID
