# pylint: disable=C0111,R0903

"""Displays information about the current song in Google Play music player.

Requires the following executable:
    * gpmdp-remote
"""

import string

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = [
            bumblebee.output.Widget(name="gpmdp.prev"),
            bumblebee.output.Widget(name="gpmdp.main", full_text=self.description),
            bumblebee.output.Widget(name="gpmdp.next"),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="playerctl previous")
        engine.input.register_callback(widgets[1], button=bumblebee.input.LEFT_MOUSE,
             cmd="playerctl play-pause")
        engine.input.register_callback(widgets[2], button=bumblebee.input.LEFT_MOUSE,
             cmd="playerctl next")

        self._status = None
        self._tags = None

    def description(self, widget):
        return self._tags if self._tags else "n/a"

    def update(self, widgets):
        self._load_song()

    def state(self, widget):
        if widget.name == "gpmdp.prev":
            return "prev"
        if widget.name == "gpmdp.next":
            return "next"
        return self._status

    def _load_song(self):
        info = ""
        try:
            info = bumblebee.util.execute("gpmdp-remote current")
            status = bumblebee.util.execute("gpmdp-remote status")
        except RuntimeError:
            pass
        self._status = status.split("\n")[0].lower()
        self._tags = info.split("\n")[0]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
