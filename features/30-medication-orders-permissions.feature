@medication-orders
Feature: Medication orders Permissions

	Scenario: Authorized to view Medication orders
		Given I have access to view Medication orders
		Then the response code should be 200

	Scenario: Not authorized to view Medication orders
		Given I do not have access to view Medication orders
		Then the response code should be 403
