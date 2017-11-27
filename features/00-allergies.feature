@use.with_use_case=ehr @allergies-and-intolerances
Feature: Allergies and intolerances

    Scenario: Correct resourceType
        Given I have a Allergies and intolerances response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @use.with_version=DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Allergies and intolerances response
        Then the resource parses as valid FHIR DSTU2 content

    @use.with_version=STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Allergies and intolerances response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Results exist
        Given I have a Allergies and intolerances response
        Then there should be at least 1 AllergyIntolerance entry

    Scenario: Resources have ids
        Given I have a Allergies and intolerances response
        And there is at least 1 AllergyIntolerance entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Allergies and intolerances response
        And there is at least 1 AllergyIntolerance entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Allergies and intolerances response
        And there is at least 1 AllergyIntolerance entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Allergies profile
        Given I have a Allergies and intolerances response
        And there is at least 1 AllergyIntolerance entry
        Then there exists one Identification of a substance, or a class of substances, that is considered to be responsible for the adverse reaction risk in AllergyIntolerance.substance
        Then there exists one reference to a Patient in AllergyIntolerance.patient
        Then there exists one status in AllergyIntolerance.status
        And AllergyIntolerance.status is bound to http://hl7.org/fhir/allergy-intolerance-status
