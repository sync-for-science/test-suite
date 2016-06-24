# S4S Testsuite

Framework for testing S4S API implementations

## Build and run in docker

    git clone https://github.com/sync-for-science/test-suite
    cd test-suite
    docker build -t tests .
    docker run --rm -it \
      -e VIRTUAL_HOST=tests.dev.syncfor.science:9003 \
      -p 5000:5000 \
      tests
      
### Develop in docker

    docker run --rm -it \
      -e VIRTUAL_HOST=tests.dev.syncfor.science:9003 \
      -p 5000:5000 \
      -v /host/path/to/test-suite \
      tests \
      /bin/bash
      
... and from inside docker, run "behave" to execute tests.

## Installation

This suite was developed for python 3. To install dependencies run `pip install -r requirements.txt`.

To configure your own project, copy `behave.ini.dist` to `behave.ini`, and change the relevant configuration values.

### Building the js app (for development)

Install npm, then `npm install` and `npm run-script build`. If you're editing
JS, you can run `npm run-script watch` to automatically re-build when files
change.

## Running the test suite

To run the suite, run `behave` with `VENDOR` like `smart` or another value from https://github.com/sync-for-science/test-suite/tree/master/config.

```
$ VENDOR=smart t behave
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

## Testing the test suite

To test the... test suite, use py.test

```
pip install -e . # Install "testsuite" so that the tests can find it
py.test
```

To see see test coverage, generate a coverage report and navigate to
/static/coverage/index.html.

```
py.test --cov=testsuite --cov-report html
```
