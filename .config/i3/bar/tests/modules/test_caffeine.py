# pylint: disable=C0103,C0111

import json
import unittest
import mock

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import tests.mocks as mocks

from bumblebee.config import Config
from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.caffeine import Module

class TestCaffeineModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)

        self.xset_active = "  timeout:  0    cycle:  123"
        self.xset_inactive = "  timeout:  600    cycle:  123"

    def tearDown(self):
        mocks.teardown_test(self)

    def test_text(self):
        self.assertEquals(self.module.caffeine(self.anyWidget), "")

    def test_active(self):
        self.popen.mock.communicate.return_value = (self.xset_active, None)
        self.assertTrue(not "deactivated" in self.module.state(self.anyWidget))
        self.assertTrue("activated" in self.module.state(self.anyWidget))

    def test_inactive(self):
        self.popen.mock.communicate.return_value = (self.xset_inactive, None)
        self.assertTrue("deactivated" in self.module.state(self.anyWidget))
        self.popen.mock.communicate.return_value = ("no text", None)
        self.assertTrue("deactivated" in self.module.state(self.anyWidget))

    def test_toggle(self):
        self.popen.mock.communicate.return_value = (self.xset_active, None)
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("xset s default")
        self.popen.assert_call("notify-send \"Out of coffee\"")
        
        self.popen.mock.communicate.return_value = (self.xset_inactive, None)
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("xset s off")
        self.popen.assert_call("notify-send \"Consuming caffeine\"")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
