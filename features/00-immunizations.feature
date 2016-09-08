@immunizations
Feature: Immunizations

    Scenario: Correct resourceType
        Given I have a Immunizations response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Immunizations response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Immunizations response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Immunizations response
        And there is at least 1 entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Immunizations response
        And there is at least 1 entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Immunizations response
        And there is at least 1 entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Immunizations profile
        Given I have a Immunizations response
        And there is at least 1 entry
        Then there exists one status in Immunization.status
        # And Immunization.status is bound to http://argonautwiki.hl7.org/index.php?title=Argonaut_Immunization_Status_Valueset
        Then there exists one dateTime in Immunization.date
        Then there exists one vaccine code in Immunization.vaccineCode
        # And Immunization.vaccineCode is bound to http://hl7.org/fhir/ValueSet/daf-cvx
        # daf-cvx is empty except for including the fhir cvx set...
        And Immunization.vaccineCode is bound to http://hl7.org/fhir/sid/cvx
        Then there exists one patient in Immunization.patient
        Then there exists one boolean value in Immunization.wasNotGiven
        Then there exists one boolean value in Immunization.reported
