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
```

## A note on `client_secret`

It is generally considered best practice to not include `client_secret` and other confidential information in public git repos. In this case however, we felt that the benefits of being able to clone this project and immediately run the test suite outweighed security concerns.

These clients are registered only to access testing environments in which no protected health information is present.
