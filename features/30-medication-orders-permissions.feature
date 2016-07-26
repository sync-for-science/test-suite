@medication-orders
Feature: Medication orders Permissions

  Scenario: Authorized to view Medication orders
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Medication orders
    And I request Medication orders
    Then the response code should be 200

  Scenario: Not authorized to view Medication orders
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Medication orders
    And I request Medication orders
    Then the response code should be 403
