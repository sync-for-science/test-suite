@medication-orders
Feature: Medication orders

    Scenario: Correct resourceType
        Given I have a Medication orders response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Medication orders response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Medication orders response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Medication orders response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Medication orders response
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Medication orders response
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Medication profile
        Given I have a Medication orders response
        Then there exists one medication in MedicationOrder.medicationCodeableConcept or MedicationOrder.medicationReference
        Then there exists one date in MedicationOrder.dateWritten
        Then there exists one status in MedicationOrder.status
        Then there exists one patient reference in MedicationOrder.patient
        Then there exists one practitioner in MedicationOrder.prescriber
