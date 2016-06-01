Feature: requesting FHIR objects

    Scenario: Conformance statements exist
        Given I am not logged in
        When I request Server metadata
        Then the response code should be 200
        And the resourceType field will be Conformance

    Scenario: Patient demographics exist
        Given I am logged in
        When I request Patient demographics
        Then the response code should be 200
        And the resourceType field will be Patient
        And all references will resolve
        And all resources will have a id field

    Scenario: Smoking status exists
        Given I am logged in
        When I request Smoking status
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Problems exist
        Given I am logged in
        When I request Problems
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Medication Orders exist
        Given I am logged in
        When I request Medication orders
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Medication Statements exist
        Given I am logged in
        When I request Medication statements
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Medication Dispensations exist
        Given I am logged in
        When I request Medication dispensations
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Medication Administrations exist
        Given I am logged in
        When I request Medication administrations
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Allergies exist
        Given I am logged in
        When I request Allergies and intolerances
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Lab results exist
        Given I am logged in
        When I request Lab results
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Vital signs exist
        Given I am logged in
        When I request Vital signs
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Procedures exist
        Given I am logged in
        When I request Procedures
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Immunizations exist
        Given I am logged in
        When I request Immunizations
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve

    Scenario: Patient documents exist
        Given I am logged in
        When I request Patient documents
        Then the response code should be 200
        And the resourceType field will be Bundle
        And the type field will be searchset
        And there should be at least 1 entry
        And all resources will have a id field
        And the total field will exist
        And all references will resolve
