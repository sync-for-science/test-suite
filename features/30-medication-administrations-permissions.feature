@medication-administrations
Feature: Medication administrations Permissions

	Scenario: Authorized to view Medication administrations
		Given I have access to view Medication administrations
		Then the response code should be 200

	Scenario: Not authorized to view Medication administrations
		Given I do not have access to view Medication administrations
		Then the response code should be 403
