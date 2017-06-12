# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in mocp.

Requires the following executable:
    * mocp

Parameters:
    * mocp.format: Format string for the song information. Tag values can be put in curly brackets (i.e. {artist})
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
            bumblebee.output.Widget(name="mocp.main", full_text=self.description),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="mocp -G")

    #@scrollable
    def description(self, widget):
        if self._running == 1:
            display =  self._status + ": " + self._artist + " - " +  self._title + " | " + self._position + "/" + self._duration
        else:
            display = "Music On Console Player"
        return display

    def update(self, widgets):
        self._load_song()

    def _load_song(self):
        try:
            info = bumblebee.util.execute("mocp -i")
            for line in info.split("\n"):
                if line.startswith("State:"):
                    self._status = line.split(": ", 2)[1]
                if line.startswith("Artist:"):
                    self._artist = line.split(": ", 2)[1]
                if line.startswith("Title:"):
                    self._title = line.split(": ", 2)[1]
                    self._title = self._title.split("(by ",2)[0]
                if line.startswith("CurrentTime:"):
                    self._position = line.split(": ", 2)[1]
                if line.startswith("TotalTime:"):
                    self._duration = line.split(": ", 2)[1]
                    self._running = 1
                if line.startswith("State: STOP"):
                    self._running = 0
        except RuntimeError:
            self._running = 0

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
