# pylint: disable=C0103,C0111

import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.cpu import Module

class TestCPUModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)
        self._psutil = mock.patch("bumblebee.modules.cpu.psutil")
        self.psutil = self._psutil.start()

    def tearDown(self):
        self._psutil.stop()
        mocks.teardown_test(self)

    def test_format(self):
        self.psutil.cpu_percent.return_value = 21.0
        self.module.update_all()
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100.00%"))

    def test_leftclick(self):
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("gnome-system-monitor")

    def test_warning(self):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "18")
        self.psutil.cpu_percent.return_value = 19.0
        self.module.update_all()
        self.assertTrue("warning" in self.module.state(self.anyWidget))

    def test_critical(self):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "19")
        self.psutil.cpu_percent.return_value = 21.0
        self.module.update_all()
        self.assertTrue("critical" in self.module.state(self.anyWidget))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
