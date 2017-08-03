@medication-statements
Feature: Medication statements

    Scenario: Correct resourceType
        Given I have a Medication statements response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Medication statements response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Medication statements response
        Then there should be at least 1 MedicationStatement entry

     Scenario: Resources have ids
        Given I have a Medication statements response
        And there is at least 1 MedicationStatement entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Medication statements response
        And there is at least 1 MedicationStatement entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Medication statements response
        And there is at least 1 MedicationStatement entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfull the Argonaut Medications profile
        Given I have a Medication statements response
        And there is at least 1 MedicationStatement entry
        Then there exists one medication in MedicationStatement.medicationCodeableConcept or MedicationStatement.medicationReference
        Then there exists one patient reference in MedicationStatement.patient
        Then there exists one status in MedicationStatement.status
        Then there exists one date or period in MedicationStatement.effectiveDateTime or MedicationStatement.effectivePeriod
