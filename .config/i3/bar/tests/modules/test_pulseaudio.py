# pylint: disable=C0103,C0111

import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE, RIGHT_MOUSE, WHEEL_UP, WHEEL_DOWN
from bumblebee.modules.pulseaudio import Module

class TestPulseAudioModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)

    def tearDown(self):
        mocks.teardown_test(self)

    def test_leftclick(self):
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("pactl set-source-mute @DEFAULT_SOURCE@ toggle")

    def test_rightclick(self):
        mocks.mouseEvent(stdin=self.stdin, button=RIGHT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("pavucontrol")

    def test_wheelup(self):
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_UP, inp=self.input, module=self.module)
        self.popen.assert_call("pactl set-source-volume @DEFAULT_SOURCE@ +2%")

    def test_wheeldown(self):
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_DOWN, inp=self.input, module=self.module)
        self.popen.assert_call("pactl set-source-volume @DEFAULT_SOURCE@ -2%")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
