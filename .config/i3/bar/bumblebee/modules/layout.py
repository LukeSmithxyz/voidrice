# pylint: disable=C0111,R0903

"""Displays and changes the current keyboard layout

Requires the following executable:
    * setxkbmap

Parameters:
    * layout.lang: pipe-separated list of languages to cycle through (e.g. us|rs|de). Default: en
"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.layout)
        )
        self._languages = self.parameter("lang", "us").split("|")
        self._idx = 0

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._next_keymap)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=self._prev_keymap)

    def _next_keymap(self, event):
        self._idx = (self._idx + 1) % len(self._languages)
        self._set_keymap()

    def _prev_keymap(self, event):
        self._idx = self._idx - 1 if self._idx > 0 else len(self._languages) - 1
        self._set_keymap()

    def _set_keymap(self):
        tmp = self._languages[self._idx].split(":")
        layout = tmp[0]
        variant = ""
        if len(tmp) > 1:
            variant = "-variant {}".format(tmp[1])
        try:
            bumblebee.util.execute("setxkbmap -layout {} {}".format(layout, variant))
        except RuntimeError:
            pass

    def layout(self, widget):
        try:
            res = bumblebee.util.execute("setxkbmap -query")
        except RuntimeError:
            return "n/a"
        layout = ""
        variant = None
        for line in res.split("\n"):
            if not line:
                continue
            if "layout" in line:
                layout = line.split(":")[1].strip()
            if "variant" in line:
                variant = line.split(":")[1].strip()
        if variant:
            layout += ":" + variant

        if layout in self._languages:
            self._idx = self._languages.index(layout)
        else:
            self._languages.append(layout)
            self._idx = len(self._languages) - 1

        return layout

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
