#!/bin/bash

# Rerun the remaps script whenever a new input device is added.

while :; do
	remaps
	grep -qP -m1 '[^un]bind.+\/[^:]+\(usb\)' <(udevadm monitor -u -t seat -s input -s usb)
done
