"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Main module implementing CLI for managing running SPARKL nodes.

This must be invoked as a package, to allow the relative import
of the command files to work:

  python -m sparkl_cli <cmd> <arg..>

Client state between invocations is maintained in the filesystem.
"""

# Uncomment the following two lines for trace debug.
# import pdb
# pdb.set_trace()

import sys

from . import (
    common,
    cmd_open,
    cmd_close)

MODULES = {
    "open":     cmd_open,
    "close":    cmd_close}


def main():
    """
    Main function performs a garbage collection of temp directories
    and then dispatches according to the command.
    """
    common.garbage_collect()

    args = common.get_args()

    common.SESSION_PID = args.session

    print common.get_working_dir()

    if args.cmd in MODULES:
        module = MODULES[args.cmd]
        module.command(args.cmd_args)
    else:
        print "Unrecognized command: " + args.cmd
        sys.exit(1)

main()
