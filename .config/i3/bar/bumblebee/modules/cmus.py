# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in cmus.

Requires the following executable:
    * cmus-remote

Parameters:
    * cmus.format: Format string for the song information. Tag values can be put in curly brackets (i.e. {artist})
"""

from collections import defaultdict

import string

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = [
            bumblebee.output.Widget(name="cmus.prev"),
            bumblebee.output.Widget(name="cmus.main", full_text=self.description),
            bumblebee.output.Widget(name="cmus.next"),
            bumblebee.output.Widget(name="cmus.shuffle"),
            bumblebee.output.Widget(name="cmus.repeat"),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -r")
        engine.input.register_callback(widgets[1], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -u")
        engine.input.register_callback(widgets[2], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -n")
        engine.input.register_callback(widgets[3], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -S")
        engine.input.register_callback(widgets[4], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -R")

        self._fmt = self.parameter("format", "{artist} - {title} {position}/{duration}")
        self._status = None
        self._shuffle = False
        self._repeat = False
        self._tags = defaultdict(lambda: '')

    @scrollable
    def description(self, widget):
        return string.Formatter().vformat(self._fmt, (), self._tags)

    def update(self, widgets):
        self._load_song()

    def state(self, widget):
        if widget.name == "cmus.shuffle":
            return "shuffle-on" if self._shuffle else "shuffle-off"
        if widget.name == "cmus.repeat":
            return "repeat-on" if self._repeat else "repeat-off"
        if widget.name == "cmus.prev":
            return "prev"
        if widget.name == "cmus.next":
            return "next"
        return self._status

    def _load_song(self):
        info = ""
        try:
            info = bumblebee.util.execute("cmus-remote -Q")
        except RuntimeError:
            pass
        self._tags = defaultdict(lambda: '')
        for line in info.split("\n"):
            if line.startswith("status"):
                self._status = line.split(" ", 2)[1]
            if line.startswith("tag"):
                key, value = line.split(" ", 2)[1:]
                self._tags.update({ key: value })
            for key in  ["duration", "position"]:
                if line.startswith(key):
                    dur = int(line.split(" ")[1])
                    self._tags.update({key:bumblebee.util.durationfmt(dur)})
            if line.startswith("set repeat "):
                self._repeat = False if "false" in line else True
            if line.startswith("set shuffle "):
                self._shuffle = False if "false" in line else True

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
