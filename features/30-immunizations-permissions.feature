@immunizations
Feature: Immunizations Permissions

	Scenario: Authorized to view Immunizations
		Given I have access to view Immunizations
		Then the response code should be 200

	Scenario: Not authorized to view Immunizations
		Given I do not have access to view Immunizations
		Then the response code should be 403
