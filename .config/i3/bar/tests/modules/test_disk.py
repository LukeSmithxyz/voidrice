# pylint: disable=C0103,C0111

import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.disk import Module

class MockVFS(object):
    def __init__(self, perc):
        self.f_blocks = 1024*1024
        self.f_frsize = 1
        self.f_bfree = self.f_blocks*(1.0 - perc/100.0)

class TestDiskModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)
        self._os = mock.patch("bumblebee.modules.disk.os")
        self.os = self._os.start()
        self.config.set("disk.path", "somepath")

    def tearDown(self):
        self._os.stop()
        mocks.teardown_test(self)

    def test_leftclick(self):
        module = Module(engine=self.engine, config={"config":self.config})
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=module)
        self.popen.assert_call("nautilus {}".format(self.module.parameter("path")))

    def test_warning(self):
        self.config.set("disk.critical", "80")
        self.config.set("disk.warning", "70")
        self.os.statvfs.return_value = MockVFS(75.0)
        self.module.update_all()
        self.assertTrue("warning" in self.module.state(self.anyWidget))

    def test_critical(self):
        self.config.set("disk.critical", "80")
        self.config.set("disk.warning", "70")
        self.os.statvfs.return_value = MockVFS(85.0)
        self.module.update_all()
        self.assertTrue("critical" in self.module.state(self.anyWidget))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
