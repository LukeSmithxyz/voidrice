#!/bin/bash

#Flashes the active window.

#Requires transset-df and a composite manager, like xcompmgr.

transset -a -m 0
sleep .1
transset -a -x 1
sleep .1
transset -a -m 0
sleep .1
transset -a -x 1
