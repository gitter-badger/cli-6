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

import os
import argparse

from . import (
    common,
    cmd_open,
    cmd_close,
    cmd_session,
    cmd_login,
    cmd_logout)

MODULES = (
    ("open", cmd_open),
    ("close", cmd_close),
    ("session", cmd_session),
    ("login", cmd_login),
    ("logout", cmd_logout))


def parse_args():
    """
    Returns the parsed command and command arguments.

    This calls out to each submodule to parse the command line
    arguments.
    """
    parser = argparse.ArgumentParser(
        prog=__package__,
        description="SPARKL command line utility.")

    parser.add_argument(
        "-s", "--session",
        type=int,
        default=os.getppid(),
        help="optional session id, defaults to invoking pid")

    subparsers = parser.add_subparsers()

    for (cmd, submodule) in MODULES:
        subparser = subparsers.add_parser(
            cmd,
            description=submodule.DESCRIPTION)
        subparser.set_defaults(
            fun=submodule.command)
        submodule.parse_args(subparser)

    return parser.parse_args()


def main():
    """
    Main function performs a garbage collection of temp directories
    and then dispatches according to the command.
    """
    common.garbage_collect()
    args = parse_args()
    common.SESSION_PID = args.session
    args.fun(args)

main()
