# pylint: disable=C0111,R0903

"""Displays network IO for interfaces.

Parameters:
    * traffic.exclude: Comma-separated list of interface prefixes to exclude (defaults to "lo,virbr,docker,vboxnet,veth")
"""

import re
import psutil
import netifaces

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        super(Module, self).__init__(engine, config, widgets)
        self._exclude = tuple(filter(len, self.parameter("exclude", "lo,virbr,docker,vboxnet,veth").split(",")))
        self._update_widgets(widgets)
        self._status = ""

    def state(self, widget):
        if "traffic.rx" in widget.name:
            return "rx"
        if "traffic.tx" in widget.name:
            return "tx"
        return self._status

    def update(self, widgets):
        self._update_widgets(widgets)

    def create_widget(self, widgets, name, txt=None, attributes={}):
        widget = self.widget(name)
        if widget: return widget

        widget = bumblebee.output.Widget(name=name)
        widget.full_text(txt)
        widgets.append(widget)

        for key in attributes:
            widget.set(key, attributes[key])

        return widget

    def _update_widgets(self, widgets):
        interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]

        counters = psutil.net_io_counters(pernic=True)
        for interface in interfaces:
            if not interface: interface = "lo"
            data = {
                "rx": counters[interface].bytes_recv,
                "tx": counters[interface].bytes_sent,
            }

            name = "traffic-{}".format(interface)

            self.create_widget(widgets, name, interface)

            for direction in ["rx", "tx"]:
                name = "traffic.{}-{}".format(direction, interface)
                widget = self.create_widget(widgets, name, attributes={"theme.minwidth": "1000.00MB"})
                prev = widget.get(direction, 0)
                speed = bumblebee.util.bytefmt(int(data[direction]) - int(prev))
                widget.full_text(speed)
                widget.set(direction, data[direction])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
