import select
import fcntl
import contextlib
import pathlib


class LineReader:
    """Async iterator class used to read lines"""

    def __init__(self, loop, file):
        self._loop = loop
        self._file = file

    @staticmethod
    async def read_line(loop, file):
        """Waits asynchronously for a line and returns it"""
        return await loop.run_in_executor(None, file.readline)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if select.select([self._file], [], [], 0)[0]:
            return self._file.readline()
        return await LineReader.read_line(self._loop, self._file)


@contextlib.contextmanager
def lock(path: pathlib.PosixPath):
    """Creates a lock file,
    a file protected from beeing used by other processes.
    (The lock file isn't the same as the file of the passed path.)

    Args:
        path (pathlib.PosixPath): path to the file
    """
    path = path.with_suffix('.lock')

    if not path.exists():
        path.touch()

    with path.open("r+") as lock_file:
        try:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)
            yield lock_file
        finally:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)
