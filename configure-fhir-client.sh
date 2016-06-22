#!/bin/bash

git clone https://github.com/smart-on-fhir/client-py validator
cd validator
git checkout 4dad888edbb007f812dba23cf21d54158b454927
git submodule update --init --recursive
git mv fhir-parser/ fhirclient/
cd fhirclient/fhir-parser
git show  e4206871b7abf2c1f988f1f6b4f1d760498b512d:fhirspec.py  > fhirspec.py
git show  e4206871b7abf2c1f988f1f6b4f1d760498b512d:Python/settings.py > settings.py
python3 generate.py
