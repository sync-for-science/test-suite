@vital-signs
Feature: Vital signs Permissions

  Scenario: Authorized to view Vital signs
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app allowing access to Vital signs
    And I request Vital signs
    Then the response code should be 200

  Scenario: Not authorized to view Vital signs
    Given OAuth is enabled
    And I am not logged in
    When I authorize the app denying access to Vital signs
    And I request Vital signs
    Then the response code should be 403
