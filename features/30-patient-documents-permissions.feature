@patient-documents
Feature: Patient documents Permissions

	Scenario: Authorized to view Patient documents
		Given I have access to view Patient documents
		Then the response code should be 200

	Scenario: Not authorized to view Patient documents
		Given I do not have access to view Patient documents
		Then the response code should be 403
