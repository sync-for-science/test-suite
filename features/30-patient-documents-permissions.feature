@patient-documents
Feature: Patient documents Permissions

  Scenario: Authorized to view Patient documents
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Patient documents
    And I request Patient documents
    Then the response code should be 200

  Scenario: Not authorized to view Patient documents
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Patient documents
    And I request Patient documents
    Then the response code should be 403
