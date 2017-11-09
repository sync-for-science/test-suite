@lab-results
Feature: Lab results

    @DSTU2 @STU3
    Scenario: Correct resourceType
        Given I have a Lab results response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Lab results response
        Then the resource parses as valid FHIR DSTU2 content

    @STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Lab results response
        Then the resource parses as valid FHIR STU3 content

    @DSTU2 @STU3
    Scenario: Results exist
        Given I have a Lab results response
        Then there should be at least 1 Observation entry

    @DSTU2 @STU3
    Scenario: Resources have ids
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then all resources will have a id field

    @DSTU2 @STU3
    Scenario: All references will resolve
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then all references will resolve

    @DSTU2 @STU3
    Scenario: There are multiple pages of results
        Given I have a Lab results response
        And there is at least 1 Observation entry
        When I follow the "next" link
        Then the response code should be 200

    @DSTU2 @STU3
    Scenario: All the codes are valid
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then all the codes will be valid

    @warning @DSTU2 @STU3
    Scenario: Resources fulfill the Argonaut Laboratory Results profile - status
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then there exists one status in Observation.status

    @warning @DSTU2 @STU3
    Scenario: Resources fulfill the Argonaut Laboratory Results profile - category
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then there exists one category in Observation.category
        And there exists a fixed Observation.category.coding.system=http://hl7.org/fhir/observation-category
        And there exists a fixed Observation.category.coding.code=laboratory

    @warning @DSTU2 @STU3
    Scenario: Resources fulfill the Argonaut Laboratory Results profile - code
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then there exists one code in Observation.code
        And there exists a fixed Observation.code.coding.system=http://loinc.org
        And Observation.code is bound to http://loinc.org
        # Then Either one Observation.value[x] or one code in Observation.DataAbsentReason

    @warning @DSTU2 @STU3
    Scenario: Resources fulfill the Argonaut Laboratory Results profile - subject
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then there exists one reference to a Patient in Observation.subject

    @warning @DSTU2 @STU3
    Scenario: Resources fulfill the Argonaut Laboratory Results profile - date and time
        Given I have a Lab results response
        And there is at least 1 Observation entry
        Then there exists one date and time in Observation.effectiveDateTime or Observation.effectivePeriod