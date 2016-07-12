@medication-administrations
Feature: Medication administrations Permissions

  Scenario: Authorized to view Medication administrations
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Medication administrations
    And I request Medication administrations
    Then the response code should be 200

  Scenario: Not authorized to view Medication administrations
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Medication administrations
    And I request Medication administrations
    Then the response code should be 403
