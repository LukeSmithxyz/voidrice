# pylint: disable=C0111,R0903

"""Displays system load.

Parameters:
    * load.warning : Warning threshold for the one-minute load average (defaults to 70% of the number of CPUs)
    * load.critical: Critical threshold for the one-minute load average (defaults to 80% of the number of CPUs)
"""

import os
import multiprocessing

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.load)
        )
        self._load = [0, 0, 0]
        try:
            self._cpus = multiprocessing.cpu_count()
        except NotImplementedError as e:
            self._cpus = 1
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-system-monitor")

    def load(self, widget):
        return "{:.02f}/{:.02f}/{:.02f}".format(
            self._load[0], self._load[1], self._load[2]
        )

    def update(self, widgets):
        self._load = os.getloadavg()

    def state(self, widget):
        return self.threshold_state(self._load[0], self._cpus*0.7, self._cpus*0.8)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
