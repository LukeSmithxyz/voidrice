# pylint: disable=C0103,C0111

import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.memory import Module

class VirtualMemory(object):
    def __init__(self, percent):
        self.percent = percent

class TestMemoryModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)
        self._psutil = mock.patch("bumblebee.modules.memory.psutil")
        self.psutil = self._psutil.start()

    def tearDown(self):
        self._psutil.stop()
        mocks.teardown_test(self)

    def test_leftclick(self):
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("gnome-system-monitor")

    def test_warning(self):
        self.config.set("memory.critical", "80")
        self.config.set("memory.warning", "70")
        self.psutil.virtual_memory.return_value = VirtualMemory(75)
        self.module.update_all()
        self.assertTrue("warning" in self.module.state(self.anyWidget))

    def test_critical(self):
        self.config.set("memory.critical", "80")
        self.config.set("memory.warning", "70")
        self.psutil.virtual_memory.return_value = VirtualMemory(81)
        self.module.update_all()
        self.assertTrue("critical" in self.module.state(self.anyWidget))

    def test_usage(self):
        rv = VirtualMemory(50)
        rv.total = 1000
        rv.available = 500
        self.psutil.virtual_memory.return_value = rv
        self.module.update_all()
        self.assertEquals("500.00B/1000.00B (50.00%)", self.module.memory_usage(self.anyWidget))
        self.assertEquals(None, self.module.state(self.anyWidget))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
