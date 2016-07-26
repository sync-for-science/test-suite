@lab-results
Feature: Lab results Permissions

  Scenario: Authorized to view Lab results
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Lab results
    And I request Lab results
    Then the response code should be 200

  Scenario: Not authorized to view Lab results
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Lab results
    And I request Lab results
    Then the response code should be 403
