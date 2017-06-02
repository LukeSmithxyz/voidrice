# pylint: disable=C0103,C0111

import unittest
import mock
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bumblebee.config import Config
from bumblebee.theme import themes
from bumblebee.engine import all_modules

class TestConfig(unittest.TestCase):
    def setUp(self):
        self._stdout = mock.patch("bumblebee.config.sys.stdout", new_callable=StringIO)
        self._stderr = mock.patch("bumblebee.config.sys.stderr", new_callable=StringIO)

        self.stdout = self._stdout.start()
        self.stderr = self._stderr.start()

        self.defaultConfig = Config()
        self.someSimpleModules = ["foo", "bar", "baz"]
        self.someAliasModules = ["foo:a", "bar:b", "baz:c"]
        self.someTheme = "some-theme"

    def tearDown(self):
        self._stdout.stop()
        self._stderr.stop()

    def test_no_modules_by_default(self):
        self.assertEquals(self.defaultConfig.modules(), [])

    def test_simple_modules(self):
        cfg = Config(["-m"] + self.someSimpleModules)
        self.assertEquals(cfg.modules(), [{
            "name": x, "module": x
        } for x in self.someSimpleModules])

    def test_alias_modules(self):
        cfg = Config(["-m"] + self.someAliasModules)
        self.assertEquals(cfg.modules(), [{
            "module": x.split(":")[0],
            "name": x.split(":")[1],
        } for x in self.someAliasModules])

    def test_parameters(self):
        cfg = Config(["-m", "module", "-p", "module.key=value"])
        self.assertEquals(cfg.get("module.key"), "value")

    def test_theme(self):
        cfg = Config(["-t", self.someTheme])
        self.assertEquals(cfg.theme(), self.someTheme)

    def test_notheme(self):
        self.assertEquals(self.defaultConfig.theme(), "default")

    def test_list_themes(self):
        with self.assertRaises(SystemExit):
            cfg = Config(["-l", "themes"])
        result = self.stdout.getvalue()
        for theme in themes():
            self.assertTrue(theme in result)

    def test_list_modules(self):
        with self.assertRaises(SystemExit):
            cfg = Config(["-l", "modules"])
        result = self.stdout.getvalue()
        for module in all_modules():
            self.assertTrue(module["name"] in result)

    def test_invalid_list(self):
        with self.assertRaises(SystemExit):
            cfg = Config(["-l", "invalid"])
        self.assertTrue("invalid choice" in "".join(self.stderr.getvalue()))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
