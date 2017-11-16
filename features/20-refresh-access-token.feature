@smart @use-refresh-token @DSTU2 @STU3
Feature: App uses a refresh token to obtain a new access token

    Scenario: Success response has all required parameters
        Given OAuth is enabled
        And I am not logged in
        When I log in
        And I ask for a new access token
        Then the response code should be 200
        And the JSON response will contain access_token
        And the JSON response will contain token_type 
        And the JSON response will contain expires_in
        And the JSON response will contain scope

    Scenario: Missing "grant_type"
        Given OAuth is enabled
        And I am not logged in
        When I log in
        And I ask for a new access token without the grant_type field
        Then the response code should not be 200

    Scenario: Missing "refresh_token"
        Given OAuth is enabled
        And I am not logged in
        When I log in
        And I ask for a new access token without the refresh_token field
        Then the response code should not be 200
