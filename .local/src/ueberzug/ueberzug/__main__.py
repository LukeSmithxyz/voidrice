#!/usr/bin/env python3
"""Usage:
    ueberzug MODULE [options]

Routines:
    layer                   Display images
    library                 Prints the path to the bash library

Layer options:
    -p, --parser <parser>  one of json, simple, bash
                           json: Json-Object per line
                           simple: Key-Values separated by a tab
                           bash: associative array dumped via `declare -p`
                           [default: json]
    -l, --loader <loader>  one of synchronous, thread, process
                           synchronous: load images right away
                           thread: load images in threads
                           process: load images in additional processes
                           [default: process]
    -s, --silent           print stderr to /dev/null


License:
    ueberzug  Copyright (C) 2018  Nico Baeurer
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.
"""
import sys

import docopt


def main():
    options = docopt.docopt(__doc__)
    module_name = options['MODULE']
    module = None

    if module_name == 'layer':
        import ueberzug.layer as layer
        module = layer
    elif module_name == 'library':
        import ueberzug.library as library
        module = library

    if module is None:
        print("Unknown module '{}'"
              .format(module_name),
              file=sys.stderr)
        return

    module.main(options)


if __name__ == '__main__':
    main()
