Feature: requesting FHIR objects

    Scenario: Secret data is secret
        Given I am not logged in
        When I request a Patient by id smart-1288992
        Then the response code should be 401

    Scenario: Patients have IDs
        Given I am logged in
        When I request a Patient by id smart-1288992
        Then the response code should be 200
        And it will have an ID

    Scenario: Bundles have the right type
        Given I am logged in
        When I search for Patients
        Then the bundle type will be searchset
