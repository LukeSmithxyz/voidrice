#!/bin/bash

tmux  -f ~/.config/Scripts/tmux.conf new-session -s "status" -d
tmux split-window -v "htop"
tmux split-window -h "speedometer -r wlp2s0"
tmux split-window -v "speedometer -r enp0s25"
tmux select-pane -t 0
tmux split-window -h "bash ~/.config/Scripts/mailsyncloop.sh"
tmux select-pane -t 0
tmux resize-pane -R 30
tmux -2 attach-session -d
