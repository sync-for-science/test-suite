@allergies-and-intolerances
Feature: Allergies and intolerances Permissions

	Scenario: Authorized to view Allergies and intolerances
		Given I have access to view Allergies and intolerances
		Then the response code should be 200

	Scenario: Not authorized to view Allergies and intolerances
		Given I do not have access to view Allergies and intolerances
		Then the response code should be 403
