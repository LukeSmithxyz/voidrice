# pylint: disable=C0111,R0903

"""Displays CPU utilization across all CPUs.

Parameters:
    * cpu.warning : Warning threshold in % of CPU usage (defaults to 70%)
    * cpu.critical: Critical threshold in % of CPU usage (defaults to 80%)
"""

try:
    import psutil
except ImportError:
    pass

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.utilization)
        )
        self._utilization = psutil.cpu_percent(percpu=False)
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-system-monitor")

    def utilization(self, widget):
        return "{:06.02f}%".format(self._utilization)

    def update(self, widgets):
        self._utilization = psutil.cpu_percent(percpu=False)

    def state(self, widget):
        return self.threshold_state(self._utilization, 70, 80)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
