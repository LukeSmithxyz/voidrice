# pylint: disable=C0103,C0111

import sys
import mock
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import tests.mocks as mocks

from bumblebee.modules.battery import Module
from bumblebee.config import Config

class TestBatteryModule(unittest.TestCase):
    def setUp(self):
        self._stdout = mock.patch("sys.stdout", new_callable=StringIO)
        self._exists = mock.patch("bumblebee.modules.battery.os.path.exists")
        self._open = mock.patch("bumblebee.modules.battery.open", create=True)

        self.stdout = self._stdout.start()
        self.exists = self._exists.start()
        self.open = self._open.start()
        self.file = mock.Mock()
        self.file.__enter__ = lambda x: self.file
        self.file.__exit__ = lambda x, a, b, c: ""
        self.open.return_value = self.file

        self.exists.return_value = True
        self.engine = mock.Mock()
        self.config = Config()
        self.module = Module(engine=self.engine, config={"config":self.config})

        self.config.set("battery.critical", "20")
        self.config.set("battery.warning", "25")
        self.criticalValue = "19"
        self.warningValue = "21"
        self.normalValue = "26"
        self.chargedValue = "96"

        for widget in self.module.widgets():
            widget.link_module(self.module)
            self.anyWidget = widget

    def tearDown(self):
        self._stdout.stop()
        self._exists.stop()
        self._open.stop()

    def test_format(self):
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100%"))

    def test_critical(self):
        self.file.read.return_value = self.criticalValue
        self.module.update_all()
        self.assertTrue("critical" in self.module.state(self.anyWidget))

    def test_warning(self):
        self.file.read.return_value = self.warningValue
        self.module.update_all()
        self.assertTrue("warning" in self.module.state(self.anyWidget))

    def test_normal(self):
        self.file.read.return_value = self.normalValue
        self.module.update_all()
        self.assertTrue(not "warning" in self.module.state(self.anyWidget))
        self.assertTrue(not "critical" in self.module.state(self.anyWidget))

    def test_overload(self):
        self.file.read.return_value = "120"
        self.module.update_all()
        self.assertTrue(not "warning" in self.module.state(self.anyWidget))
        self.assertTrue(not "critical" in self.module.state(self.anyWidget))
        self.assertEquals(self.module.capacity(self.anyWidget), "100%")

    def test_ac(self):
        self.exists.return_value = False
        self.module.update_all()
        self.assertEquals(self.module.capacity(self.anyWidget), "ac")
        self.assertTrue("AC" in self.module.state(self.anyWidget))

    def test_error(self):
        self.file.read.side_effect = IOError("failed to read")
        self.module.update_all()
        self.assertEquals(self.module.capacity(self.anyWidget), "n/a")
        self.assertTrue("critical" in self.module.state(self.anyWidget))
        self.assertTrue("unknown" in self.module.state(self.anyWidget))

    def test_charging(self):
        self.file.read.return_value = self.chargedValue
        self.module.update_all()
        self.assertTrue("charged" in self.module.state(self.anyWidget))
        self.file.read.return_value = self.normalValue
        self.module.update_all()
        self.assertTrue("charging" in self.module.state(self.anyWidget))
        
    def test_discharging(self):
        for limit in [ 10, 25, 50, 80, 100 ]:
            value = limit - 1
            self.file.read.return_value = str(value)
            self.module.update_all()
            self.file.read.return_value = "Discharging"
            self.assertTrue("discharging-{}".format(limit) in self.module.state(self.anyWidget))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
