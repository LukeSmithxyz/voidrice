import os
import pathlib


def main(options):
    directory = \
        pathlib.PosixPath(os.path.abspath(os.path.dirname(__file__))) / 'lib'
    print((directory / 'lib.sh').as_posix())
