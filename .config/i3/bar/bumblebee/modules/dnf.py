# pylint: disable=C0111,R0903

"""Displays DNF package update information (<security>/<bugfixes>/<enhancements>/<other>)

Requires the following executable:
    * dnf

Parameters:
    * dnf.interval: Time in seconds between two consecutive update checks (defaulst to 1800)

"""

import time
import threading

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

def get_dnf_info(widget):
    try:
        res = bumblebee.util.execute("dnf updateinfo")
    except RuntimeError:
        pass

    security = 0
    bugfixes = 0
    enhancements = 0
    other = 0
    for line in res.split("\n"):

        if not line.startswith(" "): continue
        elif "ecurity" in line:
            for s in line.split():
                if s.isdigit(): security += int(s)
        elif "ugfix" in line:
            for s in line.split():
                if s.isdigit(): bugfixes += int(s)
        elif "hancement" in line:
            for s in line.split():
                if s.isdigit(): enhancements += int(s)
        else:
            for s in line.split():
                if s.isdigit(): other += int(s)

    widget.set("security", security)
    widget.set("bugfixes", bugfixes)
    widget.set("enhancements", enhancements)
    widget.set("other", other)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.updates)
        super(Module, self).__init__(engine, config, widget)
        self._next_check = 0

    def updates(self, widget):
        result = []
        for t in ["security", "bugfixes", "enhancements", "other"]:
            result.append(str(widget.get(t, 0)))
        return "/".join(result)

    def update(self, widgets):
        if int(time.time()) < self._next_check:
            return
        thread = threading.Thread(target=get_dnf_info, args=(widgets[0],))
        thread.start()
        self._next_check = int(time.time()) + self.parameter("interval", 30*60)

    def state(self, widget):
        cnt = 0
        for t in ["security", "bugfixes", "enhancements", "other"]:
            cnt += widget.get(t, 0)
        if cnt == 0:
            return "good"
        if cnt > 50 or widget.get("security", 0) > 0:
            return "critical"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
