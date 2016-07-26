@medication-statements
Feature: Medication statements Permissions

  Scenario: Authorized to view Medication statements
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Medication statements
    And I request Medication statements
    Then the response code should be 200

  Scenario: Not authorized to view Medication statements
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Medication statements
    And I request Medication statements
    Then the response code should be 403
