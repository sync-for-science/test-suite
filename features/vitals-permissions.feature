@vital-signs
Feature: Vitals Permissions

    Scenario: Authorized to view Vitals
        Given I have access to view Vital signs
        Then the response code should be 200

    Scenario: Not authorized to view Vitals
        Given I do not have access to view Vital signs
        Then the response code should be 403
