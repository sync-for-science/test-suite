@procedures
Feature: Procedures Permissions

	Scenario: Authorized to view Procedures
		Given I have access to view Procedures
		Then the response code should be 200

	Scenario: Not authorized to view Procedures
		Given I do not have access to view Procedures
		Then the response code should be 403
