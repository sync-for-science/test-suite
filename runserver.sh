#!/bin/sh

flask initdb
supervisorctl start after:*
