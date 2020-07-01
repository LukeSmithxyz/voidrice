import atexit
import sys
import os
import asyncio
import signal
import pathlib
import tempfile

import ueberzug.thread as thread
import ueberzug.files as files
import ueberzug.xutil as xutil
import ueberzug.parser as parser
import ueberzug.ui as ui
import ueberzug.batch as batch
import ueberzug.action as action
import ueberzug.tmux_util as tmux_util
import ueberzug.geometry as geometry
import ueberzug.loading as loading


async def process_xevents(loop, display, windows):
    """Coroutine which processes X11 events"""
    async for event in xutil.Events(loop, display):
        windows.process_event(event)


async def process_commands(loop, shutdown_routine_factory,
                           windows, view, tools):
    """Coroutine which processes the input of stdin"""
    try:
        async for line in files.LineReader(loop, sys.stdin):
            if not line:
                break

            try:
                data = tools.parser.parse(line[:-1])
                command = action.Command(data['action'])
                await command.action_class(**data) \
                    .apply(windows, view, tools)
            except (OSError, KeyError, ValueError, TypeError) as error:
                tools.error_handler(error)
    finally:
        asyncio.ensure_future(shutdown_routine_factory())


async def query_windows(window_factory, windows, view):
    """Signal handler for SIGUSR1.
    Searches for added and removed tmux clients.
    Added clients: additional windows will be mapped
    Removed clients: existing windows will be destroyed
    """
    parent_window_infos = xutil.get_parent_window_infos()
    view.offset = tmux_util.get_offset()
    map_parent_window_id_info = {info.window_id: info
                                 for info in parent_window_infos}
    parent_window_ids = map_parent_window_id_info.keys()
    map_current_windows = {window.parent_window.id: window
                           for window in windows}
    current_window_ids = map_current_windows.keys()
    diff_window_ids = parent_window_ids ^ current_window_ids
    added_window_ids = diff_window_ids & parent_window_ids
    removed_window_ids = diff_window_ids & current_window_ids
    draw = added_window_ids or removed_window_ids

    if added_window_ids:
        windows += window_factory.create(*[
            map_parent_window_id_info.get(wid)
            for wid in added_window_ids
        ])

    if removed_window_ids:
        windows -= [
            map_current_windows.get(wid)
            for wid in removed_window_ids
        ]

    if draw:
        windows.draw()


async def reset_terminal_info(windows):
    """Signal handler for SIGWINCH.
    Resets the terminal information of all windows.
    """
    windows.reset_terminal_info()


async def shutdown(loop):
    tasks = [task for task in asyncio.Task.all_tasks()
             if task is not asyncio.tasks.Task.current_task()]
    list(map(lambda task: task.cancel(), tasks))
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def shutdown_factory(loop):
    return lambda: asyncio.ensure_future(shutdown(loop))


def setup_tmux_hooks():
    """Registers tmux hooks which are
    required to notice a change in the visibility
    of the pane this program runs in.
    Also it's required to notice new tmux clients
    displaying our pane.

    Returns:
        function which unregisters the registered hooks
    """
    events = (
        'client-session-changed',
        'session-window-changed',
        'pane-mode-changed',
        'client-detached'
    )
    lock_directory_path = pathlib.PosixPath(tempfile.gettempdir()) / 'ueberzug'
    lock_file_path = lock_directory_path / tmux_util.get_session_id()
    own_pid = str(os.getpid())
    command_template = 'kill -USR1 '

    try:
        lock_directory_path.mkdir()
    except FileExistsError:
        pass

    def update_hooks(pid_file, pids):
        pids = ' '.join(pids)
        command = command_template + pids

        pid_file.seek(0)
        pid_file.truncate()
        pid_file.write(pids)
        pid_file.flush()

        for event in events:
            if pids:
                tmux_util.register_hook(event, command)
            else:
                tmux_util.unregister_hook(event)

    def remove_hooks():
        """Removes the hooks registered by the outer function."""
        with files.lock(lock_file_path) as lock_file:
            pids = set(lock_file.read().split())
            pids.discard(own_pid)
            update_hooks(lock_file, pids)

    with files.lock(lock_file_path) as lock_file:
        pids = set(lock_file.read().split())
        pids.add(own_pid)
        update_hooks(lock_file, pids)

    return remove_hooks


def error_processor_factory(parser):
    def wrapper(exception):
        return process_error(parser, exception)
    return wrapper


def process_error(parser, exception):
    print(parser.unparse({
        'type': 'error',
        'name': type(exception).__name__,
        'message': str(exception),
        # 'stack': traceback.format_exc()
    }), file=sys.stderr)


class View:
    """Data class which holds meta data about the screen"""
    def __init__(self):
        self.offset = geometry.Distance()
        self.media = {}
        self.screen_width = 0
        self.screen_height = 0


class Tools:
    """Data class which holds helper functions, ..."""
    def __init__(self, loader, parser, error_handler):
        self.loader = loader
        self.parser = parser
        self.error_handler = error_handler


def main(options):
    display = xutil.get_display()
    screen = display.screen()
    window_infos = xutil.get_parent_window_infos()
    loop = asyncio.get_event_loop()
    executor = thread.DaemonThreadPoolExecutor(max_workers=2)
    parser_object = (parser.ParserOption(options['--parser'])
                     .parser_class())
    image_loader = (loading.ImageLoaderOption(options['--loader'])
                    .loader_class())
    error_handler = error_processor_factory(parser_object)
    view = View()
    tools = Tools(image_loader, parser_object, error_handler)
    window_factory = ui.OverlayWindow.Factory(display, view)
    windows = batch.BatchList(window_factory.create(*window_infos))
    image_loader.register_error_handler(error_handler)
    view.screen_width = screen.width_in_pixels
    view.screen_height = screen.height_in_pixels

    if tmux_util.is_used():
        atexit.register(setup_tmux_hooks())
        view.offset = tmux_util.get_offset()

    if options['--silent']:
        sys.stderr = open('/dev/null', 'w')

    with windows:
        loop.set_default_executor(executor)

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, shutdown_factory(loop))

        loop.add_signal_handler(
            signal.SIGUSR1,
            lambda: asyncio.ensure_future(query_windows(
                window_factory, windows, view)))

        loop.add_signal_handler(
            signal.SIGWINCH,
            lambda: asyncio.ensure_future(
                reset_terminal_info(windows)))

        asyncio.ensure_future(process_xevents(loop, display, windows))
        asyncio.ensure_future(process_commands(
            loop, shutdown_factory(loop),
            windows, view, tools))

        try:
            loop.run_forever()
        finally:
            loop.close()
            executor.shutdown(wait=False)
