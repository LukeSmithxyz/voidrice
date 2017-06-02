#!/bin/sh

find . -name "*.py"|xargs pylint --disable=R0903,R0201,C0330
