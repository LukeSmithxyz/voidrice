#pylint: disable=C0111,R0903

"""Displays the name, IP address(es) and status of each available network interface.

Parameters:
    * nic.exclude: Comma-separated list of interface prefixes to exclude (defaults to "lo,virbr,docker,vboxnet,veth")
"""

try:
    import netifaces
except ImportError:
    pass

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

    def update(self, widgets):
        self._update_widgets(widgets)

    def state(self, widget):
        states = []

        if widget.get("state") == "down":
            states.append("critical")
        elif widget.get("state") != "up":
            states.append("warning")

        intf = widget.get("intf")
        iftype = "wireless" if self._iswlan(intf) else "wired"
        iftype = "tunnel" if self._istunnel(intf) else iftype

        states.append("{}-{}".format(iftype, widget.get("state")))

        return states

    def _iswlan(self, intf):
        # wifi, wlan, wlp, seems to work for me
        if intf.startswith("w"): return True
        return False

    def _istunnel(self, intf):
        return intf.startswith("tun")

    def get_addresses(self, intf):
        retval = []
        try:
            for ip in netifaces.ifaddresses(intf).get(netifaces.AF_INET, []):
                if ip.get("addr", "") != "":
                    retval.append(ip.get("addr"))
        except Exception:
            return []
        return retval

    def _update_widgets(self, widgets):
        interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]

        for widget in widgets:
            widget.set("visited", False)

        for intf in interfaces:
            addr = []
            state = "down"
            for ip in self.get_addresses(intf):
                addr.append(ip)
                state = "up"
            widget = self.widget(intf)
            if not widget:
                widget = bumblebee.output.Widget(name=intf)
                widgets.append(widget)
            widget.full_text("{} {} {}".format(intf, state, ", ".join(addr)))
            widget.set("intf", intf)
            widget.set("state", state)
            widget.set("visited", True)

        for widget in widgets:
            if widget.get("visited") == False:
                widgets.remove(widget)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
