# pylint: disable=C0103,C0111

import mock
import unittest
import importlib

import tests.mocks as mocks

from bumblebee.engine import all_modules
from bumblebee.output import Widget
from bumblebee.config import Config

class TestGenericModules(unittest.TestCase):
    def setUp(self):
        engine = mock.Mock()
        engine.input = mock.Mock()
        config = Config()
        self.objects = {}

        self.popen = mocks.MockPopen()
        self.popen.mock.communicate.return_value = (str.encode("1"), "error")
        self.popen.mock.returncode = 0

        self._platform = mock.patch("bumblebee.modules.kernel.platform")
        self.platform = self._platform.start()
        self.platform.release.return_value = "unknown linux v1"

        for mod in all_modules():
            name = "bumblebee.modules.{}".format(mod["name"])
            cls = importlib.import_module(name)
            self.objects[mod["name"]] = getattr(cls, "Module")(engine, {"config": config})
            for widget in self.objects[mod["name"]].widgets():
                self.assertEquals(widget.get("variable", None), None)

    def tearDown(self):
        self._platform.stop()
        self.popen.cleanup()

    def test_widgets(self):
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            for widget in widgets:
                widget.link_module(self.objects[mod])
                self.assertEquals(widget.module, mod)
                self.assertTrue(isinstance(widget, Widget))
                self.assertTrue(hasattr(widget, "full_text"))
                widget.set("variable", "value")
                self.assertEquals(widget.get("variable", None), "value")
                self.assertTrue(isinstance(widget.full_text(), str) or isinstance(widget.full_text(), unicode))

    def test_update(self):
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            self.objects[mod].update(widgets)
            self.test_widgets()
            self.assertEquals(widgets, self.objects[mod].widgets())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
