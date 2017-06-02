"""Store interface

Allows arbitrary classes to offer a simple get/set
store interface by deriving from the Store class in
this module
"""

class Store(object):
    """Interface for storing and retrieving simple values"""
    def __init__(self):
        self._data = {}

    def set(self, key, value):
        """Set 'key' to 'value', overwriting 'key' if it exists already"""
        self._data[key] = value

    def get(self, key, default=None):
        """Return the current value of 'key', or 'default' if 'key' is not set"""
        return self._data.get(key, default)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
