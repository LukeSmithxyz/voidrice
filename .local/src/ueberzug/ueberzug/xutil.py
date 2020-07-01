"""This module contains x11 utils"""
import os
import sys
import functools
import asyncio

import Xlib
import Xlib.display as Xdisplay
import psutil

import ueberzug.tmux_util as tmux_util
import ueberzug.terminal as terminal


Xdisplay.Display.__enter__ = lambda self: self
Xdisplay.Display.__exit__ = lambda self, *args: self.close()

PREPARED_DISPLAYS = []
DISPLAY_SUPPLIES = 1


class Events:
    """Async iterator class for x11 events"""

    def __init__(self, loop, display: Xdisplay.Display):
        self._loop = loop
        self._display = display

    @staticmethod
    async def receive_event(loop, display):
        """Waits asynchronously for an x11 event and returns it"""
        return await loop.run_in_executor(None, display.next_event)

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await Events.receive_event(self._loop, self._display)


class TerminalWindowInfo(terminal.TerminalInfo):
    def __init__(self, window_id, fd_pty=None):
        super().__init__(fd_pty)
        self.window_id = window_id


async def prepare_display():
    """Fills up the display supplies."""
    if len(PREPARED_DISPLAYS) < DISPLAY_SUPPLIES:
        PREPARED_DISPLAYS.append(Xdisplay.Display())


def get_display():
    """Unfortunately, Xlib tends to produce death locks
    on requests with an expected reply.
    (e.g. Drawable#get_geometry)
    Use for each request a new display as workaround.
    """
    for _ in range(len(PREPARED_DISPLAYS), DISPLAY_SUPPLIES):
        asyncio.ensure_future(prepare_display())
    if not PREPARED_DISPLAYS:
        return Xdisplay.Display()
    return PREPARED_DISPLAYS.pop()


@functools.lru_cache()
def get_parent_pids(pid=None):
    """Determines all parent pids of this process.
    The list is sorted from youngest parent to oldest parent.
    """
    pids = []
    process = psutil.Process(pid=pid)

    while (process is not None and
           process.pid > 1):
        pids.append(process.pid)
        process = process.parent()

    return pids


def get_pid_by_window_id(display: Xdisplay.Display, window_id: int):
    window = display.create_resource_object('window', window_id)
    prop = window.get_full_property(display.intern_atom('_NET_WM_PID'),
                                    Xlib.X.AnyPropertyType)
    return (prop.value[0] if prop
            else None)


def get_pid_window_id_map():
    """Determines the pid of each mapped window.

    Returns:
        dict of {pid: window_id}
    """
    with get_display() as display:
        root = display.screen().root
        visible_window_ids = \
            (root.get_full_property(
                display.intern_atom('_NET_CLIENT_LIST'),
                Xlib.X.AnyPropertyType)
             .value)
        return {**{
            get_pid_by_window_id(display, window.id): window.id
            for window in root.query_tree().children
        }, **{
            get_pid_by_window_id(display, window_id): window_id
            for window_id in visible_window_ids
        }}


def sort_by_key_list(mapping: dict, key_list: list):
    """Sorts the items of the mapping
    by the index of the keys in the key list.

    Args:
        mapping (dict): the mapping to be sorted
        key_list (list): the list which specifies the order

    Returns:
        list: which contains the sorted items as tuples
    """
    key_map = {key: index for index, key in enumerate(key_list)}
    return sorted(
        mapping.items(),
        key=lambda item: key_map.get(item[0], float('inf')))


def key_intersection(mapping: dict, key_list: list):
    """Creates a new map which only contains the intersection
    of the keys.

    Args:
        mapping (dict): the mapping to be filtered
        key_list (list): the keys to be used as a whitelist

    Returns:
        dict: which only contains keys which are also in key_list
    """
    key_map = {key: index for index, key in enumerate(key_list)}
    return {key: value for key, value in mapping.items()
            if key in key_map}


def get_first_pty(pids: list):
    """Determines the pseudo terminal of
    the first process in the passed list which owns one.
    """
    for pid in pids:
        pty_candidate = '/proc/{pid}/fd/1'.format(pid=pid)
        with open(pty_candidate) as pty:
            if os.isatty(pty.fileno()):
                return pty_candidate

    return None


def get_parent_window_infos():
    """Determines the window id of each
    terminal which displays the program using
    this layer.

    Returns:
        list of TerminalWindowInfo
    """
    window_infos = []
    client_pids = {}

    if tmux_util.is_used():
        client_pids = tmux_util.get_client_pids()
    else:
        client_pids = {psutil.Process().pid}

    if client_pids:
        pid_window_id_map = get_pid_window_id_map()

        for pid in client_pids:
            ppids = get_parent_pids(pid)
            ppid_window_id_map = key_intersection(pid_window_id_map, ppids)
            try:
                window_pid, window_id = next(iter(sort_by_key_list(
                    ppid_window_id_map, ppids)))
                window_children_pids = ppids[:ppids.index(window_pid)][::-1]
                pty = get_first_pty(window_children_pids)
                window_infos.append(TerminalWindowInfo(window_id, pty))
            except StopIteration:
                # Window needs to be mapped,
                # otherwise it's not listed in _NET_CLIENT_LIST
                pass

    return window_infos
