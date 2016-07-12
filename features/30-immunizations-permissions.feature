@immunizations
Feature: Immunizations Permissions

  Scenario: Authorized to view Immunizations
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Immunizations
    And I request Immunizations
    Then the response code should be 200

  Scenario: Not authorized to view Immunizations
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Immunizations
    And I request Immunizations
    Then the response code should be 403
