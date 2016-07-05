@medication-statements
Feature: Medication statements Permissions

	Scenario: Authorized to view Medication statements
		Given I have access to view Medication statements
		Then the response code should be 200

	Scenario: Not authorized to view Medication statements
		Given I do not have access to view Medication statements
		Then the response code should be 403
