# pylint: disable=C0111,R0903

"""Displays the current color temperature of redshift

Requires the following executable:
    * redshift
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
        self._state = "transition"

    def text(self, widget):
        return "{}".format(self._text)

    def update(self, widgets):
        result = bumblebee.util.execute("redshift -p")

        temp = ""
        transition = ""
        for line in result.split("\n"):
            if "temperature" in line.lower():
                temp = line.split(" ")[2]
            if "period" in line.lower():
                state = line.split(" ")[1].lower()
                if "day" in state:
                    self._state = "day"
                elif "night" in state:
                    self._state = "night"
                else:
                    self._state = "transition"
                    transition = " ".join(line.split(" ")[2:])
        self._text = "{} {}".format(temp, transition)

    def state(self, widget):
        return self._state

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
