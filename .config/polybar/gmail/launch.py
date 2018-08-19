#!/usr/bin/env python

import subprocess, os

s = subprocess.check_output("nmcli networking connectivity check", shell=True)

if b'full' in s:
    os.system('~/.config/polybar/gmail/run.py')
if b'limited' in s:
    print('')

