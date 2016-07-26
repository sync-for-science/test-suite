@smoking-status
Feature: Smoking status Permissions

  Scenario: Authorized to view Smoking status
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Smoking status
    And I request Smoking status
    Then the response code should be 200

  Scenario: Not authorized to view Smoking status
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Smoking status
    And I request Smoking status
    Then the response code should be 403
