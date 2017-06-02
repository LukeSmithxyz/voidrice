# pylint: disable=C0111,R0903

"""Draws a widget with configurable text content.

Parameters:
    * spacer.text: Widget contents (defaults to empty string)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.text)
        )
        self._text = self.parameter("text", "")

    def text(self, widget):
        return self._text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
