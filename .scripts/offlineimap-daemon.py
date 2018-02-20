#!/usr/bin/env python3

import subprocess
import signal
import threading
import sys

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


class OfflineimapCtl(object):
	def __init__(self):
		self.daemon_proc = None
		self.run_ev = threading.Event()
		self.run_daemon = False

	def run(self):
		t = threading.Thread(target=self._watch_daemon, daemon=True)
		t.start()

	def _watch_daemon(self):
		while True:
			self.run_ev.wait()
			self.run_ev.clear()
			if self.run_daemon:
				self.is_running = True
				print('offlineimap is being started')
				self._spawn_daemon()
				print('offlineimap has stopped')
				self.run_ev.set() # check state and restart if needed

	def _spawn_daemon(self):
		self.daemon_proc = subprocess.Popen(['offlineimap', '-u', 'basic'], shell=False)
		self.daemon_proc.wait()
		self.daemon_proc = None

	def start(self):
		print('starting offlineimap')
		self.run_daemon = True
		self.run_ev.set()

	def stop(self):
		print('stopping offlineimap')
		self.run_daemon = False
		if self.daemon_proc:
			try:
				self.daemon_proc.send_signal(signal.SIGUSR2)
			except OSError:
				print('Unable to stop offlineimap')

	def restart(self):
		print('restarting offlineimap')
		if self.run_daemon:
			self.stop()
			self.start()

	def onConnectivityChanged(self, state):
		# 70 means fully connected
		if state == 70:
			self.start()
		else:
			self.stop()

def main():
	oi_ctl = OfflineimapCtl()
	oi_ctl.run()

	try:
		bus = dbus.SystemBus(mainloop=DBusGMainLoop())
		network_manager = bus.get_object(
			'org.freedesktop.NetworkManager',
			'/org/freedesktop/NetworkManager')
		network = dbus.Interface(network_manager,
			dbus_interface='org.freedesktop.NetworkManager')

		network.connect_to_signal('StateChanged', oi_ctl.onConnectivityChanged)

		# send current state as first event
		state = network.state()
		oi_ctl.onConnectivityChanged(state)

	except dbus.exceptions.DBusException:
		print('Unable to connect to dbus')
		sys.exit(3)

	# start receiving events from dbus
	loop = GLib.MainLoop()
	loop.run()

if __name__ == '__main__':
	main()
