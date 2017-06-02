# pylint: disable=C0103,C0111

import json
import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import I3BarInput, LEFT_MOUSE, RIGHT_MOUSE

class TestI3BarInput(unittest.TestCase):
    def setUp(self):
        self.input = I3BarInput()
        self.input.need_event = True

        self._stdin = mock.patch("bumblebee.input.sys.stdin")
        self.stdin = self._stdin.start()
        self._select = mock.patch("bumblebee.input.select")
        self.select = self._select.start()
        self.popen = mocks.MockPopen()

        self.stdin.fileno.return_value = 1
        epoll = mock.Mock()
        self.select.epoll.return_value = epoll

        epoll.poll.return_value = [(self.stdin.fileno.return_value, 2)]

        self.anyModule = mock.Mock()
        self.anyModule.id = mocks.rand(10)
        self.anotherModule = mock.Mock()
        self.anotherModule.id = mocks.rand(10)
        self.anyWidget = mocks.MockWidget("some-widget")
        self.anotherWidget = mocks.MockWidget("another-widget")
        self.anyData = self.invalidData = "any data"
        self.invalidEvent = json.dumps({"name": None, "instance": None, "button": 1})
        self.incompleteEvent = json.dumps({"button": 1})
        self.anyCommand = "this is a command with arguments"

        self._called = 0

    def tearDown(self):
        self._stdin.stop()
        self._select.stop()
        self.popen.cleanup()

    def callback(self, event):
        self._called += 1

    def calls(self):
        rv = self._called
        self._called = 0
        return rv

    def test_read_event(self):
        self.stdin.readline.return_value = self.anyData
        self.input.start()
        self.input.stop()
        self.stdin.readline.assert_any_call()

    def test_ignore_invalid_input(self):
        for data in [ self.invalidData, self.incompleteEvent, self.invalidEvent ]:
            self.stdin.readline.return_value = data
            self.input.start()
            self.assertEquals(self.input.alive(), True)
            self.assertEquals(self.input.stop(), True)
            self.stdin.readline.assert_any_call()

    def test_global_callback(self):
        self.input.register_callback(None, button=LEFT_MOUSE, cmd=self.callback)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin)
        self.assertTrue(self.calls() > 0)

    def test_remove_global_callback(self):
        self.test_global_callback()
        self.input.deregister_callbacks(None)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin)
        self.assertTrue(self.calls() == 0)

    def test_global_callback_wrong_button(self):
        self.input.register_callback(None, button=LEFT_MOUSE, cmd=self.callback)
        mocks.mouseEvent(button=RIGHT_MOUSE, inp=self.input, stdin=self.stdin)
        self.assertTrue(self.calls() == 0)

    def test_module_callback(self):
        self.input.register_callback(self.anyModule, button=LEFT_MOUSE, cmd=self.callback)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin, module=self.anyModule)
        self.assertTrue(self.calls() > 0)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin, module=self.anotherModule)
        self.assertTrue(self.calls() == 0)

    def test_remove_module_callback(self):
        self.test_module_callback()
        self.input.deregister_callbacks(self.anyModule)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin, module=self.anyModule)
        self.assertTrue(self.calls() == 0)

    def test_widget_callback(self):
        self.input.register_callback(self.anyWidget, button=LEFT_MOUSE, cmd=self.callback)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin, module=self.anyWidget)
        self.assertTrue(self.calls() > 0)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin, module=self.anotherWidget)
        self.assertTrue(self.calls() == 0)

    def test_widget_cmd_callback(self):
        self.input.register_callback(self.anyWidget, button=LEFT_MOUSE, cmd=self.anyCommand)
        mocks.mouseEvent(button=LEFT_MOUSE, inp=self.input, stdin=self.stdin, module=self.anyWidget)
        self.popen.assert_call(self.anyCommand)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
