@patient-demographics
Feature: Patient demographics Permissions

	Scenario: Authorized to view Patient demographics
		Given I have access to view Patient demographics
		Then the response code should be 200

	Scenario: Not authorized to view Patient demographics
		Given I do not have access to view Patient demographics
		Then the response code should be 403
