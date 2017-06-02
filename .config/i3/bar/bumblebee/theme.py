# pylint: disable=C0103

"""Theme support"""

import os
import glob
import copy
import json
import io

import bumblebee.error

def theme_path():
    """Return the path of the theme directory"""
    return os.path.dirname("{}/../themes/".format(os.path.dirname(os.path.realpath(__file__))))

def themes():
    result = []

    for filename in glob.iglob("{}/*.json".format(theme_path())):
        if "test" not in filename:
            result.append(os.path.basename(filename).replace(".json", ""))
    return result

class Theme(object):
    """Represents a collection of icons and colors"""
    def __init__(self, name):
        self._init(self.load(name))
        self._widget = None
        self._cycle_idx = 0
        self._cycle = {}
        self._prevbg = None

    def _init(self, data):
        """Initialize theme from data structure"""
        for iconset in data.get("icons", []):
            self._merge(data, self._load_icons(iconset))
        self._theme = data
        self._defaults = data.get("defaults", {})
        self._cycles = self._theme.get("cycle", [])
        self.reset()

    def data(self):
        """Return the raw theme data"""
        return self._theme

    def reset(self):
        """Reset theme to initial state"""
        self._cycle = self._cycles[0] if len(self._cycles) > 0 else {}
        self._cycle_idx = 0
        self._widget = None
        self._prevbg = None

    def padding(self, widget):
        """Return padding for widget"""
        return self._get(widget, "padding", "")

    def prefix(self, widget, default=None):
        """Return the theme prefix for a widget's full text"""
        padding = self.padding(widget)
        pre = self._get(widget, "prefix", None)
        return u"{}{}{}".format(padding, pre, padding) if pre else default

    def suffix(self, widget, default=None):
        """Return the theme suffix for a widget's full text"""
        padding = self._get(widget, "padding", "")
        suf = self._get(widget, "suffix", None)
        return u"{}{}{}".format(padding, suf, padding) if suf else default

    def fg(self, widget):
        """Return the foreground color for this widget"""
        return self._get(widget, "fg", None)

    def bg(self, widget):
        """Return the background color for this widget"""
        return self._get(widget, "bg", None)

    def align(self, widget):
        """Return the widget alignment"""
        return self._get(widget, "align", None)

    def minwidth(self, widget):
        """Return the minimum width string for this widget"""
        return self._get(widget, "minwidth", "")

    def separator(self, widget):
        """Return the separator between widgets"""
        return self._get(widget, "separator", None)

    def separator_fg(self, widget):
        """Return the separator's foreground/text color"""
        return self.bg(widget)

    def separator_bg(self, widget):
        """Return the separator's background color"""
        return self._prevbg

    def separator_block_width(self, widget):
        """Return the SBW"""
        return self._get(widget, "separator-block-width", None)

    def _load_icons(self, name):
        """Load icons for a theme"""
        path = "{}/icons/".format(theme_path())
        return self.load(name, path=path)

    def load(self, name, path=theme_path()):
        """Load and parse a theme file"""
        themefile = "{}/{}.json".format(path, name)

        if os.path.isfile(themefile):
            try:
                with io.open(themefile,encoding="utf-8") as data:
                    return json.load(data)
            except ValueError as exception:
                raise bumblebee.error.ThemeLoadError("JSON error: {}".format(exception))
        else:
            raise bumblebee.error.ThemeLoadError("no such theme: {}".format(name))

    def _get(self, widget, name, default=None):
        """Return the config value 'name' for 'widget'"""

        if not self._widget:
            self._widget = widget

        if self._widget != widget:
            self._prevbg = self.bg(self._widget)
            self._widget = widget
            if len(self._cycles) > 0:
                self._cycle_idx = (self._cycle_idx + 1) % len(self._cycles)
                self._cycle = self._cycles[self._cycle_idx]

        module_theme = self._theme.get(widget.module, {})
        class_theme = self._theme.get(widget.cls(), {})

        state_themes = []
        # avoid infinite recursion
        states = widget.state()
        if name not in states:
            for state in states:
                state_themes.append(self._get(widget, state, {}))

        value = self._defaults.get(name, default)
        value = widget.get("theme.{}".format(name), value)
        value = self._cycle.get(name, value)
        value = class_theme.get(name, value)
        value = module_theme.get(name, value)

        for theme in state_themes:
            value = theme.get(name, value)

        if isinstance(value, list):
            key = "{}-idx".format(name)
            idx = widget.get(key, 0)
            widget.set(key, (idx + 1) % len(value))
            value = value[idx]

        return value

    # algorithm copied from
    # http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts
    # nicely done :)
    def _merge(self, target, *args):
        """Merge two arbitrarily nested data structures"""
        if len(args) > 1:
            for item in args:
                self._merge(item)
            return target

        item = args[0]
        if not isinstance(item, dict):
            return item
        for key, value in item.items():
            if key in target and isinstance(target[key], dict):
                self._merge(target[key], value)
            else:
                target[key] = copy.deepcopy(value)
        return target

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
