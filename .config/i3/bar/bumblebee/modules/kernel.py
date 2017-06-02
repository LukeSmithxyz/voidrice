# pylint: disable=C0111,R0903

"""Shows Linux kernel version information"""

import platform

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._release_name = platform.release()

    def output(self, widget):
        return self._release_name

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
