#!/bin/sh

find themes/ -name "*.json"|grep -v invalid|xargs cat|json_verify -s
