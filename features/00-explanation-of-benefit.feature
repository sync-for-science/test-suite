@use.with_use_case=financial @use.with_version=STU3 @explanation-of-benefit
Feature: Explanation of benefit

    Scenario: Correct resourceType
        Given I have a Explanation of benefit response
        Then the resourceType field will be Bundle
        Then the type field will be searchset

    Scenario: Resources are valid FHIR STU3 content
        Given I have a Explanation of benefit response
        Then the resource parses as valid FHIR STU3 content

    Scenario: Resources fulfill the Blue Button Carrier Claim profile
        Given I have a Explanation of benefit response
        #And the response contains a Blue Button carrier claim
        Then there exists one or more business identifiers in ExplanationOfBenefit.identifier
        And each ExplanationOfBenefit.identifier must have a identifier.system
        And each ExplanationOfBenefit.identifier must have a identifier.value
        Then there exists one status in ExplanationOfBenefit.status
        Then there exists one type in ExplanationOfBenefit.type
        And there exists one or more codings in ExplanationOfBenefit.type.coding
        And each ExplanationOfBenefit.type.coding must have a coding.system
        And each ExplanationOfBenefit.type.coding must have a coding.code
        Then there exists one reference to a Patient in ExplanationOfBenefit.patient
        Then there exists one period in ExplanationOfBenefit.billablePeriod
        And each ExplanationOfBenefit.billablePeriod must have a start
        And each ExplanationOfBenefit.billablePeriod must have a end
        Then there exists one reference to a Coverage in ExplanationOfBenefit.insurance.coverage
        Then there exists one or more items in ExplanationOfBenefit.item
        And each ExplanationOfBenefit.item must have a item.sequence
        And each ExplanationOfBenefit.item must have a item.category
        And each ExplanationOfBenefit.item.category must have a category.coding
        And each ExplanationOfBenefit.item.category.coding must have a coding.system
        And each ExplanationOfBenefit.item.category.coding must have a coding.code
        And each ExplanationOfBenefit.item must have a item.service
        And each ExplanationOfBenefit.item.service.coding must have a coding.system
        And each ExplanationOfBenefit.item.service.coding must have a coding.code
        # ext
        #And each ExplanationOfBenefit.item must have a item.modifier
        #And each ExplanationOfBenefit.item.modifier.coding must have a coding.system
        #And each ExplanationOfBenefit.item.modifier.coding must have a coding.code
        And there exists one time in ExplanationOfBenefit.item.servicedDate or ExplanationOfBenefit.item.servicedPeriod
        And each ExplanationOfBenefit.item must have a item.locationCodeableConcept
        And each ExplanationOfBenefit.item.locationCodeableConcept.coding must have a coding.system
        And each ExplanationOfBenefit.item.locationCodeableConcept.coding must have a coding.code
        # ext
        And each ExplanationOfBenefit.item must have a item.quantity
        And each ExplanationOfBenefit.item.quantity must have a quantity.value
        And each ExplanationOfBenefit.item must have a item.adjudication
        And each ExplanationOfBenefit.item.adjudication must have a adjudication.category
        And each ExplanationOfBenefit.item.adjudication.category must have a category.coding
        And each ExplanationOfBenefit.item.adjudication.category.coding must have a coding.system
        And each ExplanationOfBenefit.item.adjudication.category.coding must have a coding.code
        And each ExplanationOfBenefit.item.adjudication must have a adjudication.reason
        And each ExplanationOfBenefit.item.adjudication.reason must have a reason.coding
        And each ExplanationOfBenefit.item.adjudication.reason.coding must have a coding.system
        And each ExplanationOfBenefit.item.adjudication.reason.coding must have a coding.code
        And each ExplanationOfBenefit.item.adjudication must have a adjudication.amount
        And each ExplanationOfBenefit.item.adjudication.amount must have a amount.value
        And each ExplanationOfBenefit.item.adjudication.amount must have a amount.system
        And each ExplanationOfBenefit.item.adjudication.amount must have a amount.code
        # ext
        # exts
        Then there exists one payment in ExplanationOfBenefit.payment
        And each ExplanationOfBenefit.payment must have a amount
        And each ExplanationOfBenefit.payment.amount must have a value
        And each ExplanationOfBenefit.payment.amount must have a system
        # exts
