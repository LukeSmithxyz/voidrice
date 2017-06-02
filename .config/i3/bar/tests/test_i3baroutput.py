# pylint: disable=C0103,C0111

import json
import mock
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import tests.mocks as mocks

from bumblebee.output import I3BarOutput

class TestI3BarOutput(unittest.TestCase):
    def setUp(self):
        self.theme = mock.Mock()
        self.theme.separator_fg.return_value = "#123456"
        self.theme.separator_bg.return_value = "#000000"
        self.theme.separator.return_value = ""
        self.theme.prefix.return_value = ""
        self.theme.suffix.return_value = ""
        self.theme.separator_block_width.return_value = 1
        self.theme.fg.return_value = "#ababab"
        self.theme.bg.return_value = "#ababab"
        self.theme.align.return_value = None
        self.theme.minwidth.return_value = ""
        self.output = I3BarOutput(self.theme)

        self._stdout = mock.patch("bumblebee.output.sys.stdout", new_callable=StringIO)
        self.stdout = self._stdout.start()

        self.anyWidget = mocks.MockWidget("some text")
        self.anyModule = mock.Mock()
        self.anyModule.id = mocks.rand(10)
        self.anyModule.name = mocks.rand(10)

        self.expectedStart = json.dumps({"version": 1, "click_events": True}) + "\n[\n"
        self.expectedStop = "]\n"

        self.anyColor = "#ffffff"
        self.anotherColor = "#cdcdcd"

    def tearDown(self):
        self._stdout.stop()

    def test_start(self):
        self.output.start()
        self.assertEquals(self.expectedStart, self.stdout.getvalue())

    def test_stop(self):
        self.output.stop()
        self.assertEquals(self.expectedStop, self.stdout.getvalue())

    def test_draw_single_widget(self):
        self.output.draw(self.anyWidget, self.anyModule)
        self.output.flush()
        result = json.loads(self.stdout.getvalue())[0]
        self.assertEquals(result["full_text"], self.anyWidget.full_text())

    def test_draw_multiple_widgets(self):
        for i in range(4):
            self.output.draw(self.anyWidget, self.anyModule)
        self.output.flush()
        result = json.loads(self.stdout.getvalue())
        for res in result:
            self.assertEquals(res["full_text"], self.anyWidget.full_text())

    def test_begin(self):
        self.output.begin()
        self.assertEquals("", self.stdout.getvalue())

    def test_end(self):
        self.output.end()
        self.assertEquals(",\n", self.stdout.getvalue())

    def test_prefix(self):
        self.theme.prefix.return_value = " - "
        self.output.draw(self.anyWidget, self.anyModule)
        self.output.flush()
        result = json.loads(self.stdout.getvalue())[0]
        self.assertEquals(result["full_text"], " - {}".format(self.anyWidget.full_text()))

    def test_suffix(self):
        self.theme.suffix.return_value = " - "
        self.output.draw(self.anyWidget, self.anyModule)
        self.output.flush()
        result = json.loads(self.stdout.getvalue())[0]
        self.assertEquals(result["full_text"], "{} - ".format(self.anyWidget.full_text()))

    def test_bothfix(self):
        self.theme.prefix.return_value = "*"
        self.theme.suffix.return_value = " - "
        self.output.draw(self.anyWidget, self.anyModule)
        self.output.flush()
        result = json.loads(self.stdout.getvalue())[0]
        self.assertEquals(result["full_text"], "*{} - ".format(self.anyWidget.full_text()))

    def test_colors(self):
        self.theme.fg.return_value = self.anyColor
        self.theme.bg.return_value = self.anotherColor
        self.output.draw(self.anyWidget, self.anyModule)
        self.output.flush()
        result = json.loads(self.stdout.getvalue())[0]
        self.assertEquals(result["color"], self.anyColor)
        self.assertEquals(result["background"], self.anotherColor)

    def test_widget_link(self):
        self.anyWidget.link_module(self.anyModule)
        self.assertEquals(self.anyWidget._module, self.anyModule)
        self.assertEquals(self.anyWidget.module, self.anyModule.name)

    def test_unlinked_widget_state(self):
        state = self.anyWidget.state()
        self.assertTrue(type(state) == list)

    def test_linked_widget_state(self):
        self.anyWidget.link_module(self.anyModule)
        for lst in [ "samplestate", ["a", "b", "c"], [] ]:
            self.anyModule.state.return_value = lst
            state = self.anyWidget.state()
            self.assertEquals(type(state), list)
            if type(lst) is not list: lst = [lst]
            self.assertEquals(state, lst)

    def test_widget_fulltext(self):
        self.anyWidget.full_text("some text")
        self.assertEquals(self.anyWidget.full_text(), "some text")
        self.anyWidget.full_text(lambda x: "callable fulltext")
        self.assertEquals(self.anyWidget.full_text(), "callable fulltext")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
