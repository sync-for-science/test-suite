@problems
Feature: Problems

    Scenario: Correct resourceType
        Given I have a Problems response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Problems response
        Then the resource parses as valid FHIR DSTU2 content

     Scenario: Results exist
        Given I have a Problems response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Problems response
        And there is at least 1 entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Problems response
        And there is at least 1 entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Problems response
        And there is at least 1 entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Problems and Health Concerns profile
        Given I have a Problems response
        And there is at least 1 entry
        Then there exists one Identification of the the problem or concern in Condition.code
        And Condition.code is bound to http://hl7.org/fhir/ValueSet/daf-problem
        Then there exists one patient reference in Condition.patient
        Then there exists one code in Condition.verificationStatus
        And Condition.verificationStatus is bound to http://hl7.org/fhir/ValueSet/condition-ver-status
