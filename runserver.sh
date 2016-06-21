#!/bin/sh

pip install -r requirements.txt
supervisorctl start after:*
