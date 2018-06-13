#!/bin/sh

flask initdb
flask update_bloom_filter
supervisorctl start after:*
