@problems
Feature: Problems Permissions

	Scenario: Authorized to view Problems
		Given I have access to view Problems
		Then the response code should be 200

	Scenario: Not authorized to view Problems
		Given I do not have access to view Problems
		Then the response code should be 403
