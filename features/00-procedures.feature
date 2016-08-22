@procedures
Feature: Procedures

    Scenario: Correct resourceType
        Given I have a Procedures response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Procedures response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Procedures response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Procedures response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Procedures response
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Procedures response
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Procedures profile
        Given I have a Procedures response
        Then there exists one reference to a Patient in Procedure.subject
        Then there exists one Identification of the procedure in Procedure.code
        # Or http://argonautwiki.hl7.org/index.php?title=CPT-4/HCPC_for_procedures
        And Procedure.code is bound to http://hl7.org/fhir/ValueSet/procedure-code
        Then there exists one date or a time period in Procedure.performedDateTime or Procedure.performedPeriod
        Then there exists one status code in Procedure.status
        And Procedure.status is bound to http://hl7.org/fhir/procedure-status
        Then there exists one status in Observation.status
