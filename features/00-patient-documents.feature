@use.with_use_case=ehr @patient-documents
Feature: Patient documents

    Scenario: Correct resourceType
        Given I have a Patient documents response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    @use.with_version=DSTU2
    Scenario: Resources are valid FHIR DSTU2 content
        Given I have a Patient documents response
        Then the resource parses as valid FHIR DSTU2 content

    @use.with_version=STU3
    Scenario: Resources are valid FHIR STU3 content
        Given I have a Patient documents response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Results exist
        Given I have a Patient documents response
        Then there should be at least 1 DocumentReference entry

    Scenario: Resources have ids
        Given I have a Patient documents response
        And there is at least 1 DocumentReference entry
        Then all resources will have a id field

    Scenario: All references will resolve
        Given I have a Patient documents response
        And there is at least 1 DocumentReference entry
        Then all references will resolve

    Scenario: All the codes are valid
        Given I have a Patient documents response
        And there is at least 1 DocumentReference entry
        Then all the codes will be valid

    @warning
    Scenario: Resources fulfill the Argonaut Document Access profile
        Given I have a Patient documents response
        And there is at least 1 DocumentReference entry
        Then there exists one reference to a Patient in DocumentReference.subject
        Then there exists one document type code in DocumentReference.type
        And DocumentReference.type is bound to http://hl7.org/fhir/ValueSet/c80-doc-typecodes
        Then there exists one url of the document in DocumentReference.content.attachment
        And there exists one mime type in DocumentReference.content.attachment.contentType
        # And DocumentReference.content.attachment.contentType is bound to http://www.rfc-editor.org/bcp/bcp13.txt
        And there exists one url of the document in DocumentReference.content.attachment.url
        Then there exists one format code in DocumentReference.content.format
        And DocumentReference.content.format is bound to http://hl7.org/fhir/ValueSet/formatcodes
        Then there exists one dateTime value in DocumentReference.indexed
        Then there exists one status in DocumentReference.status
        And DocumentReference.status is bound to http://hl7.org/fhir/document-reference-status
        Then there exists one identifier in DocumentReference.masterIdentifier
