# pylint: disable=C0111,R0903

"""Shows free diskspace, total diskspace and the percentage of free disk space.

Parameters:
    * disk.warning: Warning threshold in % of disk space (defaults to 80%)
    * disk.critical: Critical threshold in % of disk space (defaults ot 90%)
    * disk.path: Path to calculate disk usage from (defaults to /)
"""

import os

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.diskspace)
        )
        self._path = self.parameter("path", "/")
        self._perc = 0
        self._used = 0
        self._size = 0

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="termite -e ranger {}".format(self._path))

    def diskspace(self, widget):
        #return "{} {}/{} ({:05.02f}%)".format(self._path,
            #bumblebee.util.bytefmt(self._used),
            #bumblebee.util.bytefmt(self._size), self._perc
        #)
        #return  "{} {:05.02f}%".format(self._path, self._perc)
        return "{}".format(bumblebee.util.bytefmt(self._size - self._used))

    def update(self, widgets):
        st = os.statvfs(self._path)
        self._size = st.f_frsize*st.f_blocks
        self._used = self._size - st.f_frsize*st.f_bavail
        self._perc = 100.0*self._used/self._size

    def state(self, widget):
        return self.threshold_state(self._perc, 90, 95)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
