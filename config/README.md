# Vendor config files

Vendor config files define the FHIR API and authentication/authorization process for each of the vendors participating in the Sync For Science project.

## Format

```yaml
---
api:
  url:  # The FHIR base url
  patient:  # A patient ID to run tests against

auth:
  strategy:  # The oAuth strategy to use. One of refresh_token|client_credentials|none
  client_id:  # The oAuth client_id
  client_secret:  # The oAuth client_secret
  scope: launch/patient patient/*.read offline_access
  confidential_client:  # Should the test suite use basic auth while requesting tokens.
  token_url:  # Use when the token URL cannot be derived from a conformance statement
  sign_in_steps: []
  authorize_steps: []
```

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

## A note on `client_secret`

It is generally considered best practice to not include `client_secret` and other confidential information in public git repos. In this case however, we felt that the benefits of being able to clone this project and immediately run the test suite outweighed security concerns.

These clients are registered only to access testing environments in which no protected health information is present.
