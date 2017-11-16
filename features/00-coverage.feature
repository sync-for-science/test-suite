@coverage @STU3
Feature: Coverage

    Scenario: Correct resourceType
        Given I have a Coverage response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR STU3 content
        Given I have a Coverage response
        Then the resource parses as valid FHIR STU3 content