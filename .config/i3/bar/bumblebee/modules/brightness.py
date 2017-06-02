# pylint: disable=C0111,R0903

"""Displays the brightness of a display

Requires the following executable:
    * xbacklight

Parameters:
    * brightness.step: The amount of increase/decrease on scroll in % (defaults to 2)

"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.brightness)
        )
        self._brightness = 0

        step = self.parameter("step", 2)

        engine.input.register_callback(self, button=bumblebee.input.WHEEL_UP,
            cmd="xbacklight +{}%".format(step))
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_DOWN,
            cmd="xbacklight -{}%".format(step))

    def brightness(self, widget):
        return "{:03.0f}%".format(self._brightness)

    def update(self, widgets):
        self._brightness = float(bumblebee.util.execute("xbacklight -get"))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
