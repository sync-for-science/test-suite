Feature: Handling oauth correctly

    Scenario: Secret data is secret
        Given I am not logged in
        When I request Patient demographics
        Then the response code should be 401

    Scenario: I can log in and access secret data
        Given I am logged in
        When I request Patient demographics
        Then the response code should be 200
