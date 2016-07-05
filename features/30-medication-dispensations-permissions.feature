@medication-dispensations
Feature: Medication dispensations Permissions

	Scenario: Authorized to view Medication dispensations
		Given I have access to view Medication dispensations
		Then the response code should be 200

	Scenario: Not authorized to view Medication dispensations
		Given I do not have access to view Medication dispensations
		Then the response code should be 403
