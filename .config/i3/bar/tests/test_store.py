# pylint: disable=C0103,C0111,W0703

import unittest

from bumblebee.store import Store

class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.anyKey = "some-key"
        self.anyValue = "some-value"
        self.unsetKey = "invalid-key"

    def test_set_value(self):
        self.store.set(self.anyKey, self.anyValue)
        self.assertEquals(self.store.get(self.anyKey), self.anyValue)

    def test_get_invalid_value(self):
        result = self.store.get(self.unsetKey)
        self.assertEquals(result, None)

    def test_get_invalid_with_default_value(self):
        result = self.store.get(self.unsetKey, self.anyValue)
        self.assertEquals(result, self.anyValue)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
