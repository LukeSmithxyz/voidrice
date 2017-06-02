# pylint: disable=R0201

"""Output classes"""

import sys
import json
import uuid

import bumblebee.store

def scrollable(func):
    def wrapper(module, widget):
        text = func(module, widget)
        width = widget.get("theme.width", module.parameter("width", 30))
        widget.set("theme.minwidth", "A"*width)
        if len(text) <= width:
            return text
        # we need to shorten
        start = widget.get("scrolling.start", -1)
        direction = widget.get("scrolling.direction", "right")
        start += 1 if direction == "right" else -1
        widget.set("scrolling.start", start)
        if width + start >= len(text):
            widget.set("scrolling.direction", "left")
        if start <= 0:
            widget.set("scrolling.direction", "right")
        text = text[start:width+start]

        return text
    return wrapper

class Widget(bumblebee.store.Store):
    """Represents a single visible block in the status bar"""
    def __init__(self, full_text="", name=""):
        super(Widget, self).__init__()
        self._full_text = full_text
        self.module = None
        self._module = None
        self.name = name
        self.id = str(uuid.uuid4())

    def link_module(self, module):
        """Set the module that spawned this widget

        This is done outside the constructor to avoid having to
        pass in the module name in every concrete module implementation"""
        self.module = module.name
        self._module = module

    def cls(self):
        if not self._module:
            return None
        return self._module.__module__.replace("bumblebee.modules.", "")

    def state(self):
        """Return the widget's state"""
        if self._module and hasattr(self._module, "state"):
            states = self._module.state(self)
            if not isinstance(states, list):
                return [states]
            return states
        return []

    def full_text(self, value=None):
        """Set or retrieve the full text to display in the widget"""
        if value:
            self._full_text = value
        else:
            if callable(self._full_text):
                return self._full_text(self)
            else:
                return self._full_text

class I3BarOutput(object):
    """Manage output according to the i3bar protocol"""
    def __init__(self, theme):
        self._theme = theme
        self._widgets = []
        self._started = False

    def started(self):
        return self._started

    def start(self):
        """Print start preamble for i3bar protocol"""
        self._started = True
        sys.stdout.write(json.dumps({"version": 1, "click_events": True}) + "\n[\n")

    def stop(self):
        """Finish i3bar protocol"""
        sys.stdout.write("]\n")

    def draw(self, widget, module=None, engine=None):
        """Draw a single widget"""
        full_text = widget.full_text()
        padding = self._theme.padding(widget)
        prefix = self._theme.prefix(widget, padding)
        suffix = self._theme.suffix(widget, padding)
        minwidth = self._theme.minwidth(widget)
        if prefix:
            full_text = u"{}{}".format(prefix, full_text)
        if suffix:
            full_text = u"{}{}".format(full_text, suffix)
        separator = self._theme.separator(widget)
        if separator:
            self._widgets.append({
                u"full_text": separator,
                "separator": False,
                "color": self._theme.separator_fg(widget),
                "background": self._theme.separator_bg(widget),
                "separator_block_width": self._theme.separator_block_width(widget),
            })
        width = self._theme.minwidth(widget)
        self._widgets.append({
            u"full_text": full_text,
            "color": self._theme.fg(widget),
            "background": self._theme.bg(widget),
            "separator_block_width": self._theme.separator_block_width(widget),
            "separator": True if separator is None else False,
            "min_width": width + "A"*(len(prefix) + len(suffix)) if width else None,
            "align": self._theme.align(widget),
            "instance": widget.id,
            "name": module.id,
        })

    def begin(self):
        """Start one output iteration"""
        self._widgets = []
        self._theme.reset()

    def flush(self):
        """Flushes output"""
        sys.stdout.write(json.dumps(self._widgets))

    def end(self):
        """Finalizes output"""
        sys.stdout.write(",\n")
        sys.stdout.flush()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
