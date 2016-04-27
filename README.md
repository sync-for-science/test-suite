# S4S Testsuite

Framework for testing S4S API implementations

## Installation

This suite was developed for python 3. To install dependencies run `pip install -r requirements.txt`.

To configure your own project, copy `behave.ini.dist` to `behave.ini`, and change the relevant configuration values.

## Running the test suite

To run the suite, run `behave`.

```
$ behave -s
Feature: requesting FHIR objects

  Scenario: Secret data is secret
    Given I am not logged in                     # 0.000s
    When I request a Patient by id smart-1288992 # 0.007s
    Then the response code should be 401         # 0.000s

  Scenario: Patients have IDs
    Given I am logged in                         # 0.006s
    When I request a Patient by id smart-1288992 # 0.019s
    Then the response code should be 200         # 0.000s
    And it will have an ID                       # 0.000s

  Scenario: Bundles have the right type
    Given I am logged in                   # 0.015s
    When I search for Patients             # 0.036s
    Then the bundle type will be searchset # 0.000s

1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
10 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.085s
```
