@immunizations
Feature: Immunizations

    @DSTU2 @STU3
    Scenario: Correct resourceType
        Given I have a Immunizations response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Immunizations response
        Then the resource parses as valid FHIR DSTU2 content

    @STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Immunizations response
        Then the resource parses as valid FHIR STU3 content

    @DSTU2 @STU3
    Scenario: Results exist
        Given I have a Immunizations response
        Then there should be at least 1 Immunization entry

    @DSTU2 @STU3
    Scenario: Resources have ids
        Given I have a Immunizations response
        And there is at least 1 Immunization entry
        Then all resources will have a id field

    @DSTU2 @STU3
    Scenario: All references will resolve
        Given I have a Immunizations response
        And there is at least 1 Immunization entry
        Then all references will resolve

    @DSTU2 @STU3
    Scenario: All the codes are valid
        Given I have a Immunizations response
        And there is at least 1 Immunization entry
        Then all the codes will be valid

    @warning @DSTU2 @STU3
    Scenario: Resources fulfill the Argonaut Immunizations profile
        Given I have a Immunizations response
        And there is at least 1 Immunization entry
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
