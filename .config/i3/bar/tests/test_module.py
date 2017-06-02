# pylint: disable=C0103,C0111,W0703

import unittest

from bumblebee.engine import Module
from bumblebee.config import Config
from tests.mocks import MockWidget

class TestModule(unittest.TestCase):
    def setUp(self):
        self.widgetName = "foo"
        self.widget = MockWidget(self.widgetName)
        self.config = Config()
        self.anyWidgetName = "random-widget-name"
        self.noSuchModule = "this-module-does-not-exist"
        self.moduleWithoutWidgets = Module(engine=None, widgets=None)
        self.moduleWithOneWidget = Module(engine=None, widgets=self.widget, config={"config": self.config})
        self.moduleWithMultipleWidgets = Module(engine=None,
            widgets=[self.widget, self.widget, self.widget]
        )

        self.anyConfigName = "cfg"
        self.anotherConfigName = "cfg2"
        self.anyModule = Module(engine=None, widgets=self.widget, config={
            "name": self.anyConfigName, "config": self.config
        })
        self.anotherModule = Module(engine=None, widgets=self.widget, config={
            "name": self.anotherConfigName, "config": self.config
        })
        self.anyKey = "some-parameter"
        self.anyValue = "value"
        self.anotherValue = "another-value"
        self.emptyKey = "i-do-not-exist"
        self.config.set("{}.{}".format(self.anyConfigName, self.anyKey), self.anyValue)
        self.config.set("{}.{}".format(self.anotherConfigName, self.anyKey), self.anotherValue)

    def test_empty_widgets(self):
        self.assertEquals(self.moduleWithoutWidgets.widgets(), [])

    def test_single_widget(self):
        self.assertEquals(self.moduleWithOneWidget.widgets(), [self.widget])

    def test_multiple_widgets(self):
        for widget in self.moduleWithMultipleWidgets.widgets():
            self.assertEquals(widget, self.widget)

    def test_retrieve_widget_by_name(self):
        widget = MockWidget(self.anyWidgetName)
        widget.name = self.anyWidgetName
        module = Module(engine=None, widgets=[self.widget, widget, self.widget])
        retrievedWidget = module.widget(self.anyWidgetName)
        self.assertEquals(retrievedWidget, widget)

    def test_retrieve_widget_by_id(self):
        widget = MockWidget(self.anyWidgetName)
        widget.id = self.anyWidgetName
        module = Module(engine=None, widgets=[self.widget, widget, self.widget])
        retrievedWidget = module.widget_by_id(self.anyWidgetName)
        self.assertEquals(retrievedWidget, widget)

    def test_retrieve_missing_widget(self):
        module = self.moduleWithMultipleWidgets

        widget = module.widget(self.noSuchModule)
        self.assertEquals(widget, None)

        widget = module.widget_by_id(self.noSuchModule)
        self.assertEquals(widget, None)

    def test_threshold(self):
        module = self.moduleWithOneWidget
        module.name = self.widgetName

        self.config.set("{}.critical".format(self.widgetName), 10.0)
        self.config.set("{}.warning".format(self.widgetName), 8.0)
        self.assertEquals("critical", module.threshold_state(10.1, 0, 0))
        self.assertEquals("warning", module.threshold_state(10.0, 0, 0))
        self.assertEquals(None, module.threshold_state(8.0, 0, 0))
        self.assertEquals(None, module.threshold_state(7.9, 0, 0))

    def test_parameters(self):
        self.assertEquals(self.anyModule.parameter(self.anyKey), self.anyValue)
        self.assertEquals(self.anotherModule.parameter(self.anyKey), self.anotherValue)

    def test_default_parameters(self):
        self.assertEquals(self.anyModule.parameter(self.emptyKey), None)
        self.assertEquals(self.anyModule.parameter(self.emptyKey, self.anyValue), self.anyValue)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
