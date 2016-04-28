Feature: requesting FHIR objects

    @oauth
    Scenario: Secret data is secret
        Given I am not logged in
        When I request a Patient by id smart-1288992
        Then the response code should be 401

    @oauth
    Scenario: I can log in and access secret data
        Given I am logged in
        When I request a Patient by id smart-1288992
        Then the response code should be 200

    @oauth
    Scenario: I can revoke access tokens
        Given I am logged in
        When I revoke my access token
        And I search for Patients
        Then the response code should be 401

    @oauth
    Scenario: I can use refresh tokens to regenerate access tokens
        Given I am logged in
        When I revoke my access token
        And I refresh my access token
        And I search for Patients
        Then the response code should be 200

    Scenario: Conformance statements exist
        Given I am not logged in
        When I request a conformance statement
        Then the response code should be 200

    Scenario: Bundles have the right type
        Given I am logged in
        When I search for Patients
        Then the bundle type will be searchset
