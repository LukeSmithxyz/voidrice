# pylint: disable=C0103,C0111

import mock
import unittest

import tests.mocks as mocks

from bumblebee.util import *

class TestUtil(unittest.TestCase):
    def setUp(self):
        self.popen = mocks.MockPopen("bumblebee.util")
        self.some_command_with_args = "sample-command -a -b -c"
        self.some_utf8 = "some string".encode("utf-8")

    def tearDown(self):
        self.popen.cleanup()

    def test_bytefmt(self):
        self.assertEquals(bytefmt(10), "10.00B")
        self.assertEquals(bytefmt(15*1024), "15.00KiB")
        self.assertEquals(bytefmt(20*1024*1024), "20.00MiB")
        self.assertEquals(bytefmt(22*1024*1024*1024), "22.00GiB")
        self.assertEquals(bytefmt(35*1024*1024*1024*1024), "35840.00GiB")

    def test_durationfmt(self):
        self.assertEquals(durationfmt(00), "00:00")
        self.assertEquals(durationfmt(25), "00:25")
        self.assertEquals(durationfmt(60), "01:00")
        self.assertEquals(durationfmt(119), "01:59")
        self.assertEquals(durationfmt(3600), "01:00:00")
        self.assertEquals(durationfmt(7265), "02:01:05")

    def test_execute(self):
        execute(self.some_command_with_args)
        self.assertTrue(self.popen.mock.popen.called)
        self.popen.mock.popen.assert_call(self.some_command_with_args)
        self.assertTrue(self.popen.mock.communicate.called)

    def test_execute_nowait(self):
        execute(self.some_command_with_args, False)
        self.assertTrue(self.popen.mock.popen.called)
        self.popen.mock.popen.assert_call(self.some_command_with_args)
        self.assertFalse(self.popen.mock.communicate.called)

    def test_execute_utf8(self):
        self.popen.mock.communicate.return_value = [ self.some_utf8, None ]
        self.test_execute()

    def test_execute_error(self):
        self.popen.mock.returncode = 1

        with self.assertRaises(RuntimeError):
            execute(self.some_command_with_args)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
