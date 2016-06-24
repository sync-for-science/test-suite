#!/bin/sh
curl -X POST -H "Content-type: application/json" -d @allscripts.json https://fmhmuauthcertification.azurewebsites.net/api/ClientRegistration
