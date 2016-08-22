@vital-signs
Feature: Vital signs

    Scenario: Correct resourceType
        Given I have a Vital signs response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR content
        Given I have a Vital signs response
        Then the resource parses as valid FHIR DSTU2 content

    Scenario: Results exist
        Given I have a Vital signs response
        Then there should be at least 1 entry

    Scenario: Resources have ids
        Given I have a Vital signs response
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Vital signs response
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Vital signs response
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Vital Signs profile
        Given I have a Vital signs response
        Then there exists one status in Observation.status
        Then there exists one category in Observation.category
        And there exists a fixed Observation.category.coding.system=http://hl7.org/fhir/observation-category
        And there exists a fixed Observation.category.coding.code=vital-signs
        Then there exists one code in Observation.code
        And there exists a fixed Observation.code.coding.system=http://loinc.org
        # Should be http://argonautwiki.hl7.org/index.php?title=Argonaut_Vital_Signs but I don't have an import for compose and argonaut doesn't have a JSON version
        And Observation.code.coding.code is bound to http://hl7.org/fhir/ValueSet/daf-observation-CCDAVitalSignResult
        # Then Either one Observation.valueQuantity or, if there is no value, one code in Observation.DataAbsentReason
        # Then when using a panel code...
        Then there exists one patient in Observation.subject
        Then there exists one date and time in Observation.effectiveDateTime or Observation.effectivePeriod
