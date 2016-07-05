@vital-signs
Feature: Vital signs Permissions

	Scenario: Authorized to view Vital signs
		Given I have access to view Vital signs
		Then the response code should be 200

	Scenario: Not authorized to view Vital signs
		Given I do not have access to view Vital signs
		Then the response code should be 403
