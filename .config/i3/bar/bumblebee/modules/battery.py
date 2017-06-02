# pylint: disable=C0111,R0903

"""Displays battery status, remaining percentage and charging information.

Parameters:
    * battery.device  : The device to read information from (defaults to BAT0)
    * battery.warning : Warning threshold in % of remaining charge (defaults to 20)
    * battery.critical: Critical threshold in % of remaining charge (defaults to 10)
"""

import os

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.capacity)
        )
        battery = self.parameter("device", "BAT0")
        self._path = "/sys/class/power_supply/{}".format(battery)
        self._capacity = 100
        self._ac = False

    def capacity(self, widget):
        if self._ac:
            return "ac"
        if self._capacity == -1:
            return "n/a"
        return "{:03d}%".format(self._capacity)

    def update(self, widgets):
        widget = widgets[0]
        self._ac = False
        if not os.path.exists(self._path):
            self._ac = True
            self._capacity = 100
            return

        try:
            with open(self._path + "/capacity") as f:
                self._capacity = int(f.read())
        except IOError:
            self._capacity = -1
        self._capacity = self._capacity if self._capacity < 100 else 100

    def state(self, widget):
        state = []

        if self._capacity < 0:
            return ["critical", "unknown"]

        if self._capacity < int(self.parameter("critical", 10)):
            state.append("critical")
        elif self._capacity > int(self.parameter("great", 90)):
            state.append("great")
        elif self._capacity > int(self.parameter("good", 80)):
            state.append("good")
        elif self._capacity < int(self.parameter("warning", 20)):
            state.append("warning")
        elif self._capacity < int(self.parameter("mid", 80)):
            state.append("mid")

        if self._ac:
            state.append("AC")
        else:
            charge = ""
            with open(self._path + "/status") as f:
                charge = f.read().strip()
            if charge == "Discharging":
                state.append("discharging-{}".format(min([10, 25, 50, 80, 100] , key=lambda i:abs(i-self._capacity))))
            else:
                if self._capacity > 95:
                    state.append("charged")
                else:
                    state.append("charging")

        return state

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
