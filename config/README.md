# Vendor config files

Vendor config files define the FHIR API and authentication/authorization process for each of the vendors participating in the Sync For Science project.

## Format

```yaml
---
api:
  versions:
    DSTU2: # Specify the version of FHIR the URL below should be used for.
      url:  # The FHIR base url
      patient:  # A patient ID to run tests against

use_cases: # This defines which test 'groups' are to be run. (security, ehr, financial)
  security: DSTU2 # Define an FHIR version for each
  ehr: DSTU2

# You can use this configuration to skip individual steps, or whole features, if they don't apply to your installation.
ignored_steps:
  features/00-patient-documents.feature: # Skip a single test, use the test text from within feature file.
    - DocumentReference.type is bound to http://hl7.org/fhir/ValueSet/c80-doc-typecodes
  features/00-smoking.feature: # Skip whole feature
    - all

auth:
  versions:
    DSTU2:
      strategy:  # The oAuth strategy to use. One of refresh_token|client_credentials|none
      client_id:  # The oAuth client_id
      client_secret:  # The oAuth client_secret
      scope: launch/patient patient/*.read offline_access
      confidential_client:  # Should the test suite use basic auth while requesting tokens.
      token_url:  # Use when the token URL cannot be derived from a conformance statement
      revoke_url:  # The URL of a page where a user would revoke authorizations
      sign_in_steps: []
      authorize_steps: []
      revoke_steps: []
      browser:
        preferences:  # Preferences passed directly to the FireFox webdriver
```

## Use Cases

The Use Case block can be one of *security*, *ehr* or *financial*. This defines which tests will be run to avoid a large number of reported failures if your installation doesn't support the full complement of FHIR Resources (We don't expect them to!) *Financial* will test ExplanationOfBenefit and Coverage where *ehr* will test the Meaningful Use Common Clinical Data Set. Security is a required test for all installations.

## Versioning

The FHIR Version is used throughout the configuration to enable more complex setups where there are multiple versions of FHIR in use. The use_cases block defines what the test suite should expect the version to be for the different use case groups. For each use case it will look in the auth and api blocks for the matching version string in order to determine which parameters to use.

## Steps

We use selenium to follow the authorization process for each vendor. In order to make it easier to add new vendors and to manage their various authorization screens, the selenium code has been abstracted into a slim configuration language.

```
- element: '#username'  # a css selector
  send_keys: 'user.name123'
  optional: True
  when: deny.ResourceType
```

Each step should be a dictionary with an `element` key and an action (`send_keys` or `click`). Unless `optional` is set, an exception will be raised if the css selector defined in `element` can be found.

Steps tagged with a `when` conditional will not be run by default. They can however be toggled on in some features to selectively authorize or de-authorize some resource types. (see: `I authorize the app {action}ing access to {resource_type}` in [features.steps.oauth](https://github.com/sync-for-science/test-suite/blob/master/features/steps/oauth.py))

There are three sets of "steps" that will be run in the course of this test suite.

+ **sign_in_steps:** The steps a user takes to sign in. These are run before either the `authorize_steps` or the `revoke_steps`.
+ **authorize_steps:** The steps a user takes to authorize this app.
+ **revoke_steps:** The steps a user takes to revoke an authorization.

## A note on `client_secret`

It is generally considered best practice to not include `client_secret` and other confidential information in public git repos. In this case however, we felt that the benefits of being able to clone this project and immediately run the test suite outweighed security concerns.

These clients are registered only to access testing environments in which no protected health information is present.
