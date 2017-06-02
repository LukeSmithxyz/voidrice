# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays the temperature on the current location based on the ip

Requires the following python packages:
    * requests

Parameters:
    * weather.interval: Interval (in minutes) for updating weather information
    * weather.location: Set location (ISO 3166 country code), defaults to 'auto' for getting location from http://ipinfo.io
    * weather.unit: metric (default), kelvin, imperial
    * weather.apikey: API key from http://api.openweathermap.org
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import json
import time
try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.temperature)
        )
        self._temperature = 0
        self._apikey = self.parameter("apikey", "af7bfe22287c652d032a3064ffa44088")
        self._location = self.parameter("location", "auto")
        self._interval = int(self.parameter("interval", "15"))
        self._unit = self.parameter("unit", "metric")
        self._nextcheck = 0
        self._valid = False

    def _unit_suffix(self):
        if self._unit == "metric":
            return "C"
        if self._unit == "kelvin":
            return "K"
        if self._unit == "imperial":
            return "F"
        return ""

    def temperature(self, widget):
        if not self._valid:
            return u"?"
        return u"{}°{}".format(self._temperature, self._unit_suffix())

    def update(self, widgets):
        timestamp = int(time.time())
        if self._nextcheck < int(time.time()):
            try:
                self._nextcheck = int(time.time()) + self._interval*60
                weather_url = "http://api.openweathermap.org/data/2.5/weather?appid={}".format(self._apikey)
                weather_url = "{}&units={}".format(weather_url, self._unit)
                if self._location == "auto":
                    location_url = "http://ipinfo.io/json"
                    location = json.loads(requests.get(location_url).text)
                    coord = location["loc"].split(",")
                    weather_url = "{url}&lat={lat}&lon={lon}".format(url=weather_url, lat=coord[0], lon=coord[1])
                else:
                    weather_url = "{url}&q={city}".format(url=weather_url, city=self._location)
                weather = json.loads(requests.get(weather_url).text)
                self._temperature = int(weather['main']['temp'])
                self._valid = True
            except RequestException:
                self._valid = False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
