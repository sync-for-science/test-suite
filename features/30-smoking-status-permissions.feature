@smoking-status
Feature: Smoking status Permissions

	Scenario: Authorized to view Smoking status
		Given I have access to view Smoking status
		Then the response code should be 200

	Scenario: Not authorized to view Smoking status
		Given I do not have access to view Smoking status
		Then the response code should be 403
