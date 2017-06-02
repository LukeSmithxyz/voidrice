# pylint: disable=C0103,C0111

import mock
import unittest

import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.cmus import Module

class TestCmusModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)

        self.songTemplate = """
status {status}
file /path/to/file
duration {duration}
position {position}
tag title {title}
tag artist {artist}
tag album {album}
tag tracknumber 1
tag date 1984
tag comment comment
        """

    def tearDown(self):
        mocks.teardown_test(self)

    def test_read_song(self):
        self.popen.mock.communicate.return_value = ("song", None)
        self.module.update_all()
        self.popen.assert_call("cmus-remote -Q")

    def test_handle_runtimeerror(self):
        self.popen.mock.communicate.side_effect = RuntimeError("error loading song")
        self.module.update_all()
        self.assertEquals(self.module.description(self.anyWidget), " -  /")

    def test_format(self):
        self.popen.mock.communicate.return_value = (self.songTemplate.format(
            artist="an artist", title="a title", duration="100", position="20",
            album="an album", status="irrelevant"
        ), None)
        self.module.update_all()
        self.anyWidget.set("theme.width", 1000)
        self.assertEquals(self.module.description(self.anyWidget),
            "an artist - a title 00:20/01:40"
        )

    def test_scrollable_format(self):
        self.popen.mock.communicate.return_value = (self.songTemplate.format(
            artist="an artist", title="a title", duration="100", position="20",
            album="an album", status="irrelevant"
        ), None)
        self.module.update_all()
        self.anyWidget.set("theme.width", 10)
        self.assertEquals(self.module.description(self.anyWidget),
            "an artist - a title 00:20/01:40"[:10]
        )

    def test_repeat(self):
        self.popen.mock.communicate.return_value = ("set repeat false", None)
        self.module.update_all()
        self.assertTrue("repeat-off" in self.module.state(self.module.widget("cmus.repeat")))
        self.popen.mock.communicate.return_value = ("set repeat true", None)
        self.module.update_all()
        self.assertTrue("repeat-on" in self.module.state(self.module.widget("cmus.repeat")))

    def test_shuffle(self):
        self.popen.mock.communicate.return_value = ("set shuffle false", None)
        self.module.update_all()
        self.assertTrue("shuffle-off" in self.module.state(self.module.widget("cmus.shuffle")))
        self.popen.mock.communicate.return_value = ("set shuffle true", None)
        self.module.update_all()
        self.assertTrue("shuffle-on" in self.module.state(self.module.widget("cmus.shuffle")))

    def test_prevnext(self):
        self.assertTrue("prev" in self.module.state(self.module.widget("cmus.prev")))
        self.assertTrue("next" in self.module.state(self.module.widget("cmus.next")))

    def test_main(self):
        self.popen.mock.communicate.return_value = ("status paused", None)
        self.module.update_all()
        self.assertTrue("paused" in self.module.state(self.module.widget("cmus.main")))

        self.popen.mock.communicate.return_value = ("status playing", None)
        self.module.update_all()
        self.assertTrue("playing" in self.module.state(self.module.widget("cmus.main")))

        self.popen.mock.communicate.return_value = ("status stopped", None)
        self.module.update_all()
        self.assertTrue("stopped" in self.module.state(self.module.widget("cmus.main")))

    def test_widget(self):
        self.assertEquals(len(self.module.widgets()), 5)

        for idx, val in enumerate(["prev", "main", "next", "shuffle", "repeat"]):
            self.assertEquals(self.module.widgets()[idx].name, "cmus.{}".format(val))

    def test_interaction(self):
        events = [
            {"widget": "cmus.shuffle", "action": "cmus-remote -S"},
            {"widget": "cmus.repeat", "action": "cmus-remote -R"},
            {"widget": "cmus.next", "action": "cmus-remote -n"},
            {"widget": "cmus.prev", "action": "cmus-remote -r"},
            {"widget": "cmus.main", "action": "cmus-remote -u"},
        ]
        for event in events:
            mocks.mouseEvent(stdin=self.stdin, inp=self.input, module=self.module, instance=self.module.widget(event["widget"]).id, button=LEFT_MOUSE)
            self.popen.assert_call(event["action"])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
