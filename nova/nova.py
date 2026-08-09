#!/usr/bin/env python3

import sys

from .cli import command


if __name__ == "__main__":
    sys.exit(command(sys.argv[1:]))
