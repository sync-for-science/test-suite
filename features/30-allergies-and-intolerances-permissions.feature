@allergies-and-intolerances
Feature: Allergies and intolerances Permissions

  Scenario: Authorized to view Allergies and intolerances
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Allergies and intolerances
    And I request Allergies and intolerances
    Then the response code should be 200

  Scenario: Not authorized to view Allergies and intolerances
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Allergies and intolerances
    And I request Allergies and intolerances
    Then the response code should be 403
