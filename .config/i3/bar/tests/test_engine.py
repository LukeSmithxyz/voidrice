# pylint: disable=C0103,C0111,W0703,W0212

import shlex
import unittest

from bumblebee.error import ModuleLoadError
from bumblebee.engine import Engine
from bumblebee.config import Config
import bumblebee.input

from tests.mocks import MockOutput, MockInput

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Engine(config=Config(), output=MockOutput(), inp=MockInput())
        self.testModule = "test"
        self.testAlias = "test-alias"
        self.singleWidgetModule = [{"module": self.testModule, "name": "a"}]
        self.singleWidgetAlias = [{"module": self.testAlias, "name": "a" }]
        self.invalidModule = "no-such-module"
        self.testModuleSpec = "bumblebee.modules.{}".format(self.testModule)
        self.testModules = [
            {"module": "test", "name": "a"},
            {"module": "test", "name": "b"},
        ]

    def test_stop(self):
        self.assertTrue(self.engine.running())
        self.engine.stop()
        self.assertFalse(self.engine.running())

    def test_load_module(self):
        module = self.engine._load_module(self.testModule)
        self.assertEquals(module.__module__, self.testModuleSpec)

    def test_load_invalid_module(self):
        with self.assertRaises(ModuleLoadError):
            self.engine._load_module(self.invalidModule)

    def test_load_none(self):
        with self.assertRaises(ModuleLoadError):
            self.engine._load_module(None)

    def test_load_modules(self):
        modules = self.engine.load_modules(self.testModules)
        self.assertEquals(len(modules), len(self.testModules))
        self.assertEquals(
            [module.__module__ for module in modules],
            [self.testModuleSpec for module in modules]
        )

    def test_run(self):
        self.engine.load_modules(self.singleWidgetModule)
        try:
            self.engine.run()
        except Exception as e:
            self.fail(e)

    def test_aliases(self):
        modules = self.engine.load_modules(self.singleWidgetAlias)
        self.assertEquals(len(modules), 1)
        self.assertEquals(modules[0].__module__, self.testModuleSpec)

    def test_custom_cmd(self):
        testmodules = [
            { "name": "test", "button": "test.left-click", "action": "echo" },
            { "name": "test:alias", "button": "alias.right-click", "action": "echo2" },
        ]
        cmd = "-m"
        for test in testmodules:
            cmd += " " + test["name"]
        cmd += " -p"
        for test in testmodules:
            cmd += " " + test["button"] + "=" + test["action"]
        cfg = Config(shlex.split(cmd))
        inp = MockInput()
        engine = Engine(config=cfg, output=MockOutput(), inp=inp)

        i = 0
        for module in engine.modules():
            callback = inp.get_callback(module.id)
            self.assertTrue(callback is not None)
            self.assertEquals(callback["command"], testmodules[i]["action"])
            if "left" in testmodules[i]["button"]:
                self.assertTrue(callback["button"], bumblebee.input.LEFT_MOUSE)
            if "right" in testmodules[i]["button"]:
                self.assertTrue(callback["button"], bumblebee.input.RIGHT_MOUSE)
            i += 1

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
