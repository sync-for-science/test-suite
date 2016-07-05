@lab-results
Feature: Lab results Permissions

	Scenario: Authorized to view Lab results
		Given I have access to view Lab results
		Then the response code should be 200

	Scenario: Not authorized to view Lab results
		Given I do not have access to view Lab results
		Then the response code should be 403
