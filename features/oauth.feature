Feature: Handling oauth correctly

    Scenario: Secret data is secret
        Given I am not logged in
        When I request Patient demographics
        Then the response code should be 401

    Scenario: I can log in and access secret data
        Given I am logged in
        When I request Patient demographics
        Then the response code should be 200

    Scenario: I can revoke access tokens
        Given I am logged in
        When I revoke my access token
        And I request Patient demographics
        Then the response code should be 401

    Scenario: I can use refresh tokens to regenerate access tokens
        Given I am logged in
        When I revoke my access token
        And I refresh my access token
        And I request Patient demographics
        Then the response code should be 200
