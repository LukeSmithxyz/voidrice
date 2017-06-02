# pylint: disable=C0103,C0111

import json
import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.load import Module

class TestLoadModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)

        self._mp = mock.patch("bumblebee.modules.load.multiprocessing")
        self._os = mock.patch("bumblebee.modules.load.os")

        self.mp = self._mp.start()
        self.os = self._os.start()

        self.mp.cpu_count.return_value = 1

    def tearDown(self):
        self._mp.stop()
        self._os.stop()
        mocks.teardown_test(self)

    def test_leftclick(self):
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("gnome-system-monitor")

    def test_load_format(self):
        self.os.getloadavg.return_value = [ 5.9, 1.2, 0.8 ]
        self.module.update_all()
        self.assertEquals(self.module.load(self.anyWidget), "5.90/1.20/0.80")

    def test_warning(self):
        self.config.set("load.critical", "1")
        self.config.set("load.warning", "0.8")
        self.os.getloadavg.return_value = [ 0.9, 0, 0 ]
        self.module.update_all()
        self.assertTrue("warning" in self.module.state(self.anyWidget))

    def test_critical(self):
        self.config.set("load.critical", "1")
        self.config.set("load.warning", "0.8")
        self.os.getloadavg.return_value = [ 1.1, 0, 0 ]
        self.module.update_all()
        self.assertTrue("critical" in self.module.state(self.anyWidget))

    def test_assume_single_core(self):
        self.mp.cpu_count.side_effect = NotImplementedError
        module = Module(engine=self.engine, config={"config": mock.Mock() })
        self.assertEquals(1, module._cpus)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
