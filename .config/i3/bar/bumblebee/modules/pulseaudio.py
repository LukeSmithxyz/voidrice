# pylint: disable=C0111,R0903

"""Displays volume and mute status of PulseAudio devices.

Aliases: pasink, pasource

Requires the following executable:
    * pactl
"""

import re

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

ALIASES = [ "pasink", "pasource" ]

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.volume)
        )

        self._left = 0
        self._right = 0
        self._mono = 0
        self._mute = False
        channel = "sink" if self.name == "pasink" else "source"

        self._patterns = [
            { "expr": "Name:", "callback": (lambda line: False) },
            { "expr": "Mute:", "callback": (lambda line: self.mute(False if " no" in line.lower() else True)) },
            { "expr": "Volume:", "callback": self.getvolume },
        ]

        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd="pavucontrol")

        events = [
            { "type": "mute", "action": "toggle", "button": bumblebee.input.LEFT_MOUSE },
            { "type": "volume", "action": "+2%", "button": bumblebee.input.WHEEL_UP },
            { "type": "volume", "action": "-2%", "button": bumblebee.input.WHEEL_DOWN },
        ]

        for event in events:
            engine.input.register_callback(self, button=event["button"],
                cmd="pactl set-{}-{} @DEFAULT_{}@ {}".format(channel, event["type"],
                    channel.upper(), event["action"]))

    def mute(self, value):
        self._mute = value

    def getvolume(self, line):
        if "mono" in line:
            m = re.search(r'mono:.*\s*\/\s*(\d+)%', line)
            if m:
                self._mono = m.group(1)
        else:
            m = re.search(r'left:.*\s*\/\s*(\d+)%.*right:.*\s*\/\s*(\d+)%', line)
            if m:
                self._left = m.group(1)
                self._right = m.group(2)
        return True

    def _default_device(self):
        output = bumblebee.util.execute("pactl info")
        pattern = "Default Sink: " if self.name == "pasink" else "Default Source: "
        for line in output.split("\n"):
            if line.startswith(pattern):
                return line.replace(pattern, "")
        return "n/a"

    def volume(self, widget):
        if int(self._mono) > 0:
            return "{}%".format(self._mono)
        elif self._left == self._right:
            return "{}%".format(self._left)
        else:
            return "{}%/{}%".format(self._left, self._right)
        return "n/a"

    def update(self, widgets):
        channel = "sinks" if self.name == "pasink" else "sources"
        device = self._default_device()

        result = bumblebee.util.execute("pactl list {}".format(channel))
        found = False

        for line in result.split("\n"):
            if device in line:
                found = True
                continue
            if found == False:
                continue
            for pattern in self._patterns:
                if not pattern["expr"] in line:
                    continue
                if pattern["callback"](line) == False and found == True:
                    return

    def state(self, widget):
        if self._mute:
            return [ "warning", "muted" ]
        return [ "unmuted" ]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
