# Important Note

These cronjobs have components that require information about your current display to display notifications correctly.

When you add them as cronjobs, I recommend you precede the command with commands as those below:

```
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus; export DISPLAY=:0; . $HOME/.profile;  then_command_goes_here
```

This ensures that notifications will display, xdotool commands will function and environmental varialbes will work as well.
