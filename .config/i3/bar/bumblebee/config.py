"""Configuration handling

This module provides configuration information (loaded modules,
module parameters, etc.) to all other components
"""

import os
import sys
import logging
import argparse
import textwrap
import importlib
import bumblebee.store

MODULE_HELP = "Specify a space-separated list of modules to load. The order of the list determines their order in the i3bar (from left to right). Use <module>:<alias> to provide an alias in case you want to load the same module multiple times, but specify different parameters."
THEME_HELP = "Specify the theme to use for drawing modules"
PARAMETER_HELP = "Provide configuration parameters in the form of <module>.<key>=<value>"
LIST_HELP = "Display a list of either available themes or available modules along with their parameters."
DEBUG_HELP = "Enable debug log ('debug.log' located in the same directory as the bumblebee-status executable)"

class print_usage(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        argparse.Action.__init__(self, option_strings, dest, nargs, **kwargs)
        self._indent = " "*2

    def __call__(self, parser, namespace, value, option_string=None):
        if value == "modules":
            self.print_modules()
        elif value == "themes":
            self.print_themes()
        sys.exit(0)

    def print_themes(self):
        print(textwrap.fill(", ".join(bumblebee.theme.themes()),
            80, initial_indent = self._indent, subsequent_indent = self._indent
        ))

    def print_modules(self):
        for m in bumblebee.engine.all_modules():
            mod = importlib.import_module("bumblebee.modules.{}".format(m["name"]))
            print(textwrap.fill("{}:".format(m["name"]), 80,
                    initial_indent=self._indent*2, subsequent_indent=self._indent*2))
            for line in mod.__doc__.split("\n"):
                print(textwrap.fill(line, 80,
                    initial_indent=self._indent*3, subsequent_indent=self._indent*6))

def create_parser():
    """Create the argument parser"""
    parser = argparse.ArgumentParser(description="display system data in the i3bar")
    parser.add_argument("-m", "--modules", nargs="+", default=[],
        help=MODULE_HELP)
    parser.add_argument("-t", "--theme", default="default", help=THEME_HELP)
    parser.add_argument("-p", "--parameters", nargs="+", default=[],
        help=PARAMETER_HELP)
    parser.add_argument("-l", "--list", choices=["modules", "themes"], action=print_usage,
        help=LIST_HELP)
    parser.add_argument("-d", "--debug", action="store_true",
        help=DEBUG_HELP)
    parser.add_argument("-f", "--logfile", default="~/bumblebee-status-debug.log",
        help="Location of the debug log file")

    return parser

class Config(bumblebee.store.Store):
    """Top-level configuration class

    Parses commandline arguments and provides non-module
    specific configuration information.
    """
    def __init__(self, args=None):
        super(Config, self).__init__()
        parser = create_parser()
        self._args = parser.parse_args(args if args else [])

        if not self._args.debug:
            logger = logging.getLogger().disabled = True

        for param in self._args.parameters:
            key, value = param.split("=")
            self.set(key, value)

    def modules(self):
        """Return a list of all activated modules"""
        return [{
            "module": x.split(":")[0],
            "name": x if not ":" in x else x.split(":")[1],
        } for x in self._args.modules]

    def theme(self):
        """Return the name of the selected theme"""
        return self._args.theme
    
    def debug(self):
        return self._args.debug

    def logfile(self):
        return self._args.logfile

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
