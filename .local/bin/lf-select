#!/bin/sh

# Reads file names from stdin and selects them in lf.

while read -r file; do
	[ -z "$file" ] && continue
	lf -remote "send select \"$file\""
	lf -remote "send toggle"
done
