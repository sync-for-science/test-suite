@problems
Feature: Problems Permissions

  Scenario: Authorized to view Problems
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Problems
    And I request Problems
    Then the response code should be 200

  Scenario: Not authorized to view Problems
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Problems
    And I request Problems
    Then the response code should be 403
