@s4s
Feature: Implements all the S4S requirements

    Scenario: Server implements Patient demographics
        Given I have a valid conformance statement
        And this server supports Patient demographics

    Scenario: Server implements Smoking status
        Given I have a valid conformance statement
        And this server supports Smoking status

    Scenario: Server implements Problems
        Given I have a valid conformance statement
        And this server supports Problems

    Scenario: Server implements Medications
        Given I have a valid conformance statement
        And this server supports at least one of
            | type                       |
            | Medication orders          |
            | Medication statements      |
            | Medication dispensations   |
            | Medication administrations |

    Scenario: Server implements Allergies and intolerances
        Given I have a valid conformance statement
        And this server suppports Allergies and intolerances

    Scenario: Server implements Lab results
        Given I have a valid conformance statement
        And this server supports Lab results

    Scenario: Server implements Vital signs
        Given I have a valid conformance statement
        And this server supports Vital signs

    Scenario: Server implements Procedures
        Given I have a valid conformance statement
        And this server supports Procedures

    Scenario: Server implements Immunizations
        Given I have a valid conformance statement
        And this server supports Immunizations

    Scenario: Server implements Patient documents
        Given I have a valid conformance statement
        And this server supports Patient documents
