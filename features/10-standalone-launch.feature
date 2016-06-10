@smart
Feature: Follows the SMART standalone launch sequence

    Scenario: App asks for authorization - missing "response_type"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization without the response_type field
        Then the response code should not be 200

    Scenario: App asks for authorization - missing "client_id"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization without the client_id field
        Then the response code should not be 200

    Scenario: App asks for authorization - missing "redirect_uri"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization without the redirect_uri field
        Then the response code should not be 200

    Scenario: App asks for authorization - misssing "scope"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization without the scope field
        Then the response code should not be 200

    Scenario: App asks for authorization - missing "state"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization without the state field
        Then the response code should not be 200

    Scenario: App uses a refresh token to obtain a new access token
        Given OAuth is enabled
        And I am logged in
        When I ask for a new access token
        Then the response code should be 200
        And the JSON response will contain access_token
        And the JSON response will contain token_type 
        And the JSON response will contain expires_in
        And the JSON response will contain scope

    Scenario: App uses a refresh token to obtain a new access token - missing "grant_type"
        Given OAuth is enabled
        And I am logged in
        When I ask for a new access token without the grant_type field
        Then the response code should not be 200

    Scenario: App uses a refresh token to obtain a new access token - missing "refresh_token"
        Given OAuth is enabled
        And I am logged in
        When I ask for a new access token without the refresh_token field
        Then the response code should not be 200
