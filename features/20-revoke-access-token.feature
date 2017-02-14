@smart @revoke-authorization
Feature: User revokes authorization

    Scenario: User revokes authorization
        Given OAuth is enabled
        And revoking authorizations is enabled
        And I am logged in
        And I have access to Patient demographics
        When I revoke my authorization
        And I ask for a new access token
        Then the response code should not be 200
