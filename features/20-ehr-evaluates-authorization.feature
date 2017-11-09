@smart @evaluate-request @DSTU2 @STU3
Feature: EHR evaluates authorization request

    Scenario: Very long "state"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization with the following override
            | key | value |
            | state | Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla mollis libero interdum mi eleifend mollis. Phasellus velit lectus, feugiat eu turpis a, efficitur auctor leo. Praesent sed bibendum nisi, vel mollis dui. Nulla volutpat tortor in erat laoreet sodales. Nunc ex dolor, vehicula eget convallis non, volutpat a odio. Aenean nec rutrum nibh. Suspendisse fermentum sem a enim aliquet, non rhoncus dui faucibus. |
        Then the authorization response redirect should validate

    Scenario: Special characters in "state"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization with the following override
            | key | value |
            | state | `%2B~!@#$%^&*()-_=+[{]}\;:'",<.>/? |
        Then the authorization response redirect should validate

    Scenario: UTF-8 characters in "state"
        Given OAuth is enabled
        And I am not logged in
        When I ask for authorization with the following override
            | key | value |
            | state | ‘’“”✓☃èÉéÊ¿¡Ææ汉语 |
        Then the authorization response redirect should validate

    Scenario: Authorization request is aborted
        Given OAuth is enabled
        And I am not logged in
        When I abort an authorization request
        Then the authorization error response error code should be "access_denied"
