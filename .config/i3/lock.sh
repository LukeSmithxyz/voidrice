#!/bin/bash
#!/bin/bash

# Approximate timeout rate in milliseconds (checked every 5 seconds).
timeout="10000"

# Take a screenshot of every screen available:
xdpyinfo -ext XINERAMA | sed '/^  head #/!d;s///' |
{
  while IFS=' :x@,' read i w h x y; do
    INDEX=$i
    import -window root -crop ${w}x$h+$x+$y /tmp/head_$i.png
  done

# Add the lock to the swirled and blurred images:
  for i in `seq 0 ${INDEX}`;
    do
      convert /tmp/head_${i}.png -paint 1 -swirl 360 ~/.config/i3/lock.png -gravity center -composite -matte /tmp/head_${i}.png;
    done
}

#Combine all screen images into one big image
convert +append /tmp/head_*.png /tmp/screen.png

# Pause music (mocp and mpd):
mocp -P
mpc pause

# Lock it up!
i3lock -e -f -c 000000 -i /tmp/screen.png

# If still locked after $timeout milliseconds, turn off screen.
while [[ $(pgrep -x i3lock) ]]; do
  [[ $timeout -lt $(xssstate -i) ]] && xset dpms force off
  sleep 5
done
