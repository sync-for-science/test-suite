@refactor
@medication-administrations
Feature: Medication administrations

    Scenario: Correct resourceType
        Given I have a Medication administrations response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources have ids
        Given I have a Medication administrations response
        Then all resources will have a id field

    Scenario: Required search fields exist
        Given I have a Medication administrations response
        Then the total field will exist

    Scenario: All references will resolve
        Given I have a Medication administrations response
        Then all references will resolve
