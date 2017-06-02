# pylint: disable=C0111,R0903

"""Draws an error widget.
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.text)
        )
        self._text = ""

    def set(self, text):
        self._text = text

    def text(self, widget):
        return self._text

    def state(self, widget):
        return ["critical"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
