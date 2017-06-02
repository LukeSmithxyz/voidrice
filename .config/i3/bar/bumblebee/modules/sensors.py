"""Displays sensor temperature

Requires the following executable:
    * sensors

Parameters:
    * sensors.match: What line in the output of `sensors -u` should be matched against (default: temp1_input)
    * sensors.match_number: which of the matches you want (default -1: last match).
"""

import os
import re

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.temperature)
        )
        self._temperature = "unknown"
        pattern = self.parameter("match", "temp1_input")
        pattern_string = r"^\s*{}:\s*([\d.]+)$".format(pattern)
        self._match_number = int(self.parameter("match_number", "-1"))
        self._pattern = re.compile(pattern_string, re.MULTILINE)
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd="xsensors")

    def get_temp(self):
        temperatures = bumblebee.util.execute("sensors -u")
        matching_temp = self._pattern.findall(temperatures)
        temperature = "unknown"
        if matching_temp:
            temperature = int(float(matching_temp[self._match_number]))

        return temperature

    def temperature(self, widget):
        return self._temperature

    def update(self, widgets):
        self._temperature = self.get_temp()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
