# pylint: disable=C0111,R0903

"""Enable/disable automatic screen locking.

Requires the following executables:
    * xset
    * notify-send
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.caffeine)
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._toggle
        )

    def caffeine(self, widget):
        return ""

    def state(self, widget):
        if self._active():
            return "activated"
        return "deactivated"

    def _active(self):
        for line in bumblebee.util.execute("xset q").split("\n"):
            if "timeout" in line:
                timeout = int(line.split(" ")[4])
                if timeout == 0:
                    return True
                return False
        return False

    def _toggle(self, widget):
        if self._active():
            bumblebee.util.execute("xset s default")
            bumblebee.util.execute("notify-send \"Out of coffee\"")
        else:
            bumblebee.util.execute("xset s off")
            bumblebee.util.execute("notify-send \"Consuming caffeine\"")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
