#!/bin/sh

if [ "$(systemctl is-active bluetooth.service)" = "active" ]; then
    echo "#1"
else
    echo "#2"
fi
