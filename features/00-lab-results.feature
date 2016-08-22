@lab-results
Feature: Lab results

    Scenario: Correct resourceType
        Given I have a Lab results response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Lab results response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Lab results response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Lab results response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Lab results response
        Then all references will resolve

    Scenario: There are multiple pages of results
        Given I have a Lab results response
        When I follow the "next" link
        Then the response code should be 200

    Scenario: All the codes are valid
        Given I have a Lab results response
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Laboratory Results profile
        Given I have a Lab results response
        Then there exists one status in Observation.status
        Then there exists one category in Observation.category
        And there exists a fixed Observation.category.coding.system=http://hl7.org/fhir/observation-category
        And there exists a fixed Observation.category.coding.code=laboratory
        Then there exists one code in Observation.code
        And there exists a fixed Observation.code.coding.system=http://loinc.org
        And Observation.code.coding.code is bound to http://loinc.org/
        # Then Either one Observation.value[x] or one code in Observation.DataAbsentReason
        Then there exists one reference to a Patient in Observation.subject
        Then there exists one date and time in Observation.effectiveDateTime or Observation.effectivePeriod
