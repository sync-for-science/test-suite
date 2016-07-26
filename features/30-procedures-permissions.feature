@procedures
Feature: Procedures Permissions

  Scenario: Authorized to view Procedures
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Procedures
    And I request Procedures
    Then the response code should be 200

  Scenario: Not authorized to view Procedures
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Procedures
    And I request Procedures
    Then the response code should be 403
