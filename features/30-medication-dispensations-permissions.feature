@medication-dispensations
Feature: Medication dispensations Permissions

  Scenario: Authorized to view Medication dispensations
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Medication dispensations
    And I request Medication dispensations
    Then the response code should be 200

  Scenario: Not authorized to view Medication dispensations
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Medication dispensations
    And I request Medication dispensations
    Then the response code should be 403
