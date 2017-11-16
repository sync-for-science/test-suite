@s4s
Feature: Implements all the S4S requirements

    @DSTU2 @STU3
    Scenario: Server implements Patient demographics
        Given I have a valid conformance statement
        And this server supports Patient demographics

    @DSTU2 @STU3
    Scenario: Server implements Smoking status
        Given I have a valid conformance statement
        And this server supports Smoking status

    @DSTU2 @STU3
    Scenario: Server implements Problems
        Given I have a valid conformance statement
        And this server supports Problems

    @DSTU2
    Scenario: Server implements Medications
        Given I have a valid conformance statement
        And this server supports at least one of
            | type                       |
            | Medication orders          |
            | Medication statements      |
            | Medication dispensations   |
            | Medication administrations |

    @STU3
    Scenario: Server implements Medications
        Given I have a valid conformance statement
        And this server supports at least one of
            | type                       |
            | Medication requests        |
            | Medication statements      |
            | Medication dispensations   |
            | Medication administrations |

    @DSTU2 @STU3
    Scenario: Server implements Allergies and intolerances
        Given I have a valid conformance statement
        And this server supports Allergies and intolerances

    @DSTU2 @STU3
    Scenario: Server implements Lab results
        Given I have a valid conformance statement
        And this server supports Lab results

    @DSTU2 @STU3
    Scenario: Server implements Vital signs
        Given I have a valid conformance statement
        And this server supports Vital signs

    @DSTU2 @STU3
    Scenario: Server implements Procedures
        Given I have a valid conformance statement
        And this server supports Procedures

    @DSTU2 @STU3
    Scenario: Server implements Immunizations
        Given I have a valid conformance statement
        And this server supports Immunizations

    @DSTU2 @STU3
    Scenario: Server implements Patient documents
        Given I have a valid conformance statement
        And this server supports Patient documents
