#!/bin/bash

ffmpeg \
-f pulse -ac 2 -ar 48000 -i alsa_output.pci-0000_00_1b.0.analog-stereo.monitor \
-f pulse -ac 1 -ar 44100 -i alsa_input.usb-Blue_Microphones_Yeti_Stereo_Microphone_REV8-00.analog-stereo \
-filter_complex amix=inputs=2 \
-f x11grab -r 30 -s 1280x800 -i :0.0+0,0 \
-vcodec libx264 -preset fast -crf 18 \
-acodec libmp3lame -ar 44100 -q:a 1 \
-pix_fmt yuv420p \
this_output.mkv
