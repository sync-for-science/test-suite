#!/bin/sh

flask initdb
flask get_bloom_filter
supervisorctl start after:*
