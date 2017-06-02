"""get volume level

"""
import re

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.volume)
        )
        self._level = "0"
        self._muted = True
        device = self.parameter("device", "Master,0")
        self._cmdString = "amixer get {}".format(device)

    def volume(self, widget):
        m = re.search(r'([\d]+)\%', self._level)
        self._muted = True
        if m:
            if m.group(1) != "0":
                self._muted = False
            return "{}%".format(m.group(1))
        else:
            return "0%"

    def update(self, widgets):
        self._level = bumblebee.util.execute(self._cmdString)

    def state(self, widget):
        if self._muted:
            return [ "warning", "muted" ]
        return [ "unmuted" ]
