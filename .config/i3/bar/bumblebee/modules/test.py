# pylint: disable=C0111,R0903

"""Test module
"""

import bumblebee.engine

ALIASES = [ "test-alias" ]

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text="test")
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
