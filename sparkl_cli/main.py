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
    cmd_connect,
    cmd_close,
    cmd_session,
    cmd_login,
    cmd_logout,
    cmd_list,
    cmd_get)

MODULES = (
    ("connect", cmd_connect),
    ("close", cmd_close),
    ("session", cmd_session),
    ("login", cmd_login),
    ("logout", cmd_logout),
    ("list", cmd_list),
    ("get", cmd_get))


def parse_args():
    """
    Returns the parsed command and command arguments.

    This calls out to each submodule to parse the command line
    arguments.
    """
    prog_name = os.environ.get("SPARKL_PROG_NAME", None)
    if not prog_name:
        prog_name = __package__

    epilog = "Use '{ProgName} <cmd> -h' for subcommand help".format(
        ProgName=prog_name)

    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="SPARKL command line utility.",
        epilog=epilog)

    parser.add_argument(
        "-a", "--alias",
        type=str,
        default="default",
        help="optional alias for multiple connections")

    parser.add_argument(
        "-s", "--session",
        type=int,
        default=os.getppid(),
        help="optional session id, defaults to invoking pid")

    subparsers = parser.add_subparsers()

    for (cmd, submodule) in MODULES:
        subparser = subparsers.add_parser(
            cmd,
            description=submodule.DESCRIPTION,
            epilog="(Choose connection with toplevel option -a/--alias)")
        subparser.set_defaults(
            fun=submodule.command)
        submodule.parse_args(subparser)

    return parser.parse_args()


def main():
    """
    Main function performs a garbage collection of temp directories.

    It sets the common.GLOBAL values, and then dispatches according
    to the command.
    """
    common.garbage_collect()
    args = parse_args()
    common.SESSION_PID = args.session
    common.ALIAS = args.alias
    args.fun(args)

# Allow invocation using `python -m sparkl_cli.main`
if __name__ == "__main__":
    main()
