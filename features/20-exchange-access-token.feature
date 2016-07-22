@smart @exchange-code
Feature: App exchanges authorization code for access token

    Scenario: Success response has all required parameters
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code
        Then the response code should be 200
        And the JSON response will contain access_token
        And the JSON response will contain token_type
        And the JSON response will contain scope

    Scenario: Missing "grant_type"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code without the grant_type field
        Then the response code should not be 200

    Scenario: Missing "code"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code without the code field
        Then the response code should not be 200

    Scenario: Missing "redirect_uri"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code without the redirect_uri field
        Then the response code should not be 200

    Scenario: Wrong "grant_type"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code with the following override
            | key | value |
            | grant_type | Hugh |
        Then the response code should not be 200

    Scenario: Wrong "code"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code with the following override
            | key | value |
            | code | WURVFXGJYTHEIZXSQXOBGSVRUDOOJXATBKT |
        Then the response code should not be 200

    Scenario: Wrong "redirect_uri"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization
        And I exchange my authorization code with the following override
            | key | value |
            | redirect_uri | https://example.com |
        Then the response code should not be 200
