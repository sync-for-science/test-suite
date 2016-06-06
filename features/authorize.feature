@authorize
Feature: Can automatically authorize

    Scenario: Authorization happens
        Given I am not logged in
        When I authorize
