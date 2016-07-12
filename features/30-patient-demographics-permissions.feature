@patient-demographics
Feature: Patient demographics Permissions

  Scenario: Authorized to view Patient demographics
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Patient demographics
    And I request Patient demographics
    Then the response code should be 200

  Scenario: Not authorized to view Patient demographics
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Patient demographics
    And I request Patient demographics
    Then the response code should be 403
