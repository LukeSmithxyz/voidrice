# pylint: disable=C0103,C0111,W0703

import mock
import unittest
from bumblebee.theme import Theme
from bumblebee.error import ThemeLoadError
from tests.mocks import MockWidget

class TestTheme(unittest.TestCase):
    def setUp(self):
        self.nonexistentThemeName = "no-such-theme"
        self.invalidThemeName = "test_invalid"
        self.validThemeName = "test"
        self.validThemeSeparator = " * "
        self.themedWidget = MockWidget("bla")
        self.theme = Theme(self.validThemeName)
        self.cycleTheme = Theme("test_cycle")
        self.anyModule = mock.Mock()
        self.anyWidget = MockWidget("bla")
        self.anotherWidget = MockWidget("blub")

        self.anyModule.state.return_value = "state-default"

        self.anyWidget.link_module(self.anyModule)
        self.themedWidget.link_module(self.anyModule)

        data = self.theme.data()
        self.widgetTheme = "test-widget"
        self.themedWidget.module = self.widgetTheme
        self.defaultColor = data["defaults"]["fg"]
        self.defaultBgColor = data["defaults"]["bg"]
        self.widgetColor = data[self.widgetTheme]["fg"]
        self.widgetBgColor = data[self.widgetTheme]["bg"]
        self.defaultPrefix = data["defaults"]["prefix"]
        self.defaultSuffix = data["defaults"]["suffix"]
        self.widgetPrefix = data[self.widgetTheme]["prefix"]
        self.widgetSuffix = data[self.widgetTheme]["suffix"]

    def test_load_valid_theme(self):
        try:
            Theme(self.validThemeName)
        except Exception as e:
            self.fail(e)

    def test_load_nonexistent_theme(self):
        with self.assertRaises(ThemeLoadError):
            Theme(self.nonexistentThemeName)

    def test_load_invalid_theme(self):
        with self.assertRaises(ThemeLoadError):
            Theme(self.invalidThemeName)

    def test_default_prefix(self):
        self.assertEquals(self.theme.prefix(self.anyWidget), self.defaultPrefix)

    def test_default_suffix(self):
        self.assertEquals(self.theme.suffix(self.anyWidget), self.defaultSuffix)

    def test_widget_prefix(self):
        self.assertEquals(self.theme.prefix(self.themedWidget), self.widgetPrefix)

    def test_widget_fg(self):
        self.assertEquals(self.theme.fg(self.anyWidget), self.defaultColor)
        self.anyWidget.module = self.widgetTheme
        self.assertEquals(self.theme.fg(self.anyWidget), self.widgetColor)

    def test_widget_bg(self):
        self.assertEquals(self.theme.bg(self.anyWidget), self.defaultBgColor)
        self.anyWidget.module = self.widgetTheme
        self.assertEquals(self.theme.bg(self.anyWidget), self.widgetBgColor)

    def test_absent_cycle(self):
        theme = self.theme
        try:
            theme.fg(self.anyWidget)
            theme.fg(self.anotherWidget)
        except Exception as e:
            self.fail(e)

    def test_reset(self):
        theme = self.cycleTheme
        data = theme.data()
        theme.reset()
        self.assertEquals(theme.fg(self.anyWidget), data["cycle"][0]["fg"])
        self.assertEquals(theme.fg(self.anotherWidget), data["cycle"][1]["fg"])
        theme.reset()
        self.assertEquals(theme.fg(self.anyWidget), data["cycle"][0]["fg"])

    def test_separator_block_width(self):
        theme = self.theme
        data = theme.data()

        self.assertEquals(theme.separator_block_width(self.anyWidget),
            data["defaults"]["separator-block-width"]
        )

    def test_separator(self):
        for theme in [self.theme, self.cycleTheme]:
            theme.reset()
            prev_bg = theme.bg(self.anyWidget)
            theme.bg(self.anotherWidget)

            self.assertEquals(theme.separator_fg(self.anotherWidget), theme.bg(self.anotherWidget))
            self.assertEquals(theme.separator_bg(self.anotherWidget), prev_bg)

    def test_state(self):
        theme = self.theme
        data = theme.data()

        self.assertEquals(theme.fg(self.anyWidget), data["defaults"]["fg"])
        self.assertEquals(theme.bg(self.anyWidget), data["defaults"]["bg"])

        self.anyModule.state.return_value = "critical"
        self.assertEquals(theme.fg(self.anyWidget), data["defaults"]["critical"]["fg"])
        self.assertEquals(theme.bg(self.anyWidget), data["defaults"]["critical"]["bg"])
        self.assertEquals(theme.fg(self.themedWidget), data[self.widgetTheme]["critical"]["fg"])
        # if elements are missing in the state theme, they are taken from the
        # widget theme instead (i.e. no fallback to a more general state theme)
        self.assertEquals(theme.bg(self.themedWidget), data[self.widgetTheme]["bg"])

    def test_separator(self):
        self.assertEquals(self.validThemeSeparator, self.theme.separator(self.anyWidget))

    def test_list(self):
        theme = self.theme
        data = theme.data()[self.widgetTheme]["cycle-test"]["fg"]
        self.anyModule.state.return_value = "cycle-test"
        self.assertTrue(len(data) > 1)

        for idx in range(0, len(data)):
            self.assertEquals(theme.fg(self.themedWidget), data[idx])
        self.assertEquals(theme.fg(self.themedWidget), data[0])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
