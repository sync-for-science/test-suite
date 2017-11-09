@medication-requests @STU3
Feature: Medication requests

    Scenario: Correct resourceType
        Given I have a Medication requests response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR STU3 content
        Given I have a Medication requests response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Results exist
        Given I have a Medication requests response
        Then there should be at least 1 MedicationRequest entry

    Scenario: Resources have ids
        Given I have a Medication requests response
        And there is at least 1 MedicationRequest entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Medication requests response
        And there is at least 1 MedicationRequest entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Medication requests response
        And there is at least 1 MedicationRequest entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Medication profile
        Given I have a Medication requests response
        And there is at least 1 MedicationRequest entry
        Then there exists one medication in MedicationRequest.medicationCodeableConcept or MedicationRequest.medicationReference
        Then there exists one date in MedicationRequest.dateWritten
        Then there exists one status in MedicationRequest.status
        Then there exists one patient reference in MedicationRequest.subject
        Then there exists one practitioner in MedicationRequest.prescriber
