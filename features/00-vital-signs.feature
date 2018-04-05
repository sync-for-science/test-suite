@use.with_use_case=ehr @vital-signs
Feature: Vital signs

    Scenario: Correct resourceType
        Given I have a Vital signs response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @use.with_version=DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Vital signs response
        Then the resource parses as valid FHIR DSTU2 content

    @use.with_version=STU3
    Scenario: Resources are valid STU3 content
        Given I have a Vital signs response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Results exist
        Given I have a Vital signs response
        Then there should be at least 1 Observation entry

    Scenario: Resources have ids
        Given I have a Vital signs response
        And there is at least 1 Observation entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Vital signs response
        And there is at least 1 Observation entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Vital signs response
        And there is at least 1 Observation entry
        Then all the codes will be valid

    Scenario: Observations have a value or DataAbsentReason
        Given I have a Vital signs response
        And there is at least 1 Observation entry
        Then one of the following paths exist: valueQuantity.value,component.valueQuantity.value,DataAbsentReason in Observation

    @warning
    Scenario: Resources fulfill the Argonaut Vital Signs profile
        Given I have a Vital signs response
        And there is at least 1 Observation entry
        Then there is at least one entry with a fixed Observation.category.coding.code=vital-signs
        Then there exists one status in Observation.status
        Then there exists one category in Observation.category
        And there exists a fixed Observation.category.coding.system=http://hl7.org/fhir/observation-category
        And there exists a fixed Observation.category.coding.code=vital-signs
        Then there exists one code in Observation.code
        And there exists a fixed Observation.code.coding.system=http://loinc.org
        And Observation.code is bound to http://fhir.org/guides/argonaut/ValueSet/observation-ccdavitalsignresult
        # Then when using a panel code...
        Then there exists one patient in Observation.subject
        Then there exists one date and time in Observation.effectiveDateTime or Observation.effectivePeriod
