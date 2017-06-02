"""Input classes"""

import sys
import json
import uuid
import time
import select
import threading
import bumblebee.util

LEFT_MOUSE = 1
MIDDLE_MOUSE = 2
RIGHT_MOUSE = 3
WHEEL_UP = 4
WHEEL_DOWN = 5

def is_terminated():
    for thread in threading.enumerate():
        if thread.name == "MainThread" and not thread.is_alive():
            return True
    return False

def read_input(inp):
    """Read i3bar input and execute callbacks"""
    epoll = select.epoll()
    epoll.register(sys.stdin.fileno(), select.EPOLLIN)
    while inp.running:
        if is_terminated():
            return

        events = epoll.poll(1)
        for fileno, event in events:
            line = "["
            while "[" in line:
                line = sys.stdin.readline().strip(",").strip()
            inp.has_event = True
            try:
                event = json.loads(line)
                if "instance" in event:
                    inp.callback(event)
                    inp.redraw()
            except ValueError:
                pass
    epoll.unregister(sys.stdin.fileno())
    epoll.close()
    inp.has_event = True
    inp.clean_exit = True

class I3BarInput(object):
    """Process incoming events from the i3bar"""
    def __init__(self):
        self.running = True
        self._callbacks = {}
        self.clean_exit = False
        self.global_id = str(uuid.uuid4())
        self.need_event = False
        self.has_event = False
        self._condition = threading.Condition()

    def start(self):
        """Start asynchronous input processing"""
        self.has_event = False
        self.running = True
        self._condition.acquire()
        self._thread = threading.Thread(target=read_input, args=(self,))
        self._thread.start()

    def redraw(self):
        self._condition.acquire()
        self._condition.notify()
        self._condition.release()

    def alive(self):
        """Check whether the input processing is still active"""
        return self._thread.is_alive()

    def wait(self, timeout):
        self._condition.wait(timeout)

    def _wait(self):
        while not self.has_event:
            time.sleep(0.1)
        self.has_event = False

    def stop(self):
        """Stop asynchronous input processing"""
        self._condition.release()
        if self.need_event:
            self._wait()
        self.running = False
        self._thread.join()
        return self.clean_exit

    def _uuidstr(self, name, button):
        return "{}::{}".format(name, button)

    def _uid(self, obj, button):
        uid = self.global_id
        if obj:
            uid = obj.id
        return self._uuidstr(uid, button)

    def deregister_callbacks(self, obj):
        to_delete = []
        uid = obj.id if obj else self.global_id
        for key in self._callbacks:
            if uid in key:
                to_delete.append(key)
        for key in to_delete:
            del self._callbacks[key]

    def register_callback(self, obj, button, cmd):
        """Register a callback function or system call"""
        uid = self._uid(obj, button)
        if uid not in self._callbacks:
            self._callbacks[uid] = {}
        self._callbacks[uid] = cmd

    def callback(self, event):
        """Execute callback action for an incoming event"""
        button = event["button"]

        cmd = self._callbacks.get(self._uuidstr(self.global_id, button), None)
        cmd = self._callbacks.get(self._uuidstr(event["name"], button), cmd)
        cmd = self._callbacks.get(self._uuidstr(event["instance"], button), cmd)

        if cmd is None:
            return
        if callable(cmd):
            cmd(event)
        else:
            bumblebee.util.execute(cmd, False)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
