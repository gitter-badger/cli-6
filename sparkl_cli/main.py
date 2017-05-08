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
from __future__ import print_function

import os
import sys
import argparse
import pkg_resources

from sparkl_cli.common import (
    get_args,
    garbage_collect)

from sparkl_cli import (
    cli_exception,
    cmd_connect,
    cmd_close,
    cmd_session,
    cmd_login,
    cmd_logout,
    cmd_ls,
    cmd_get,
    cmd_put,
    cmd_rm,
    cmd_show,
    cmd_mkdir,
    cmd_undo,
    cmd_vars,
    cmd_call,
    cmd_listen)

MODULES = (
    ("connect", cmd_connect, "Create or show connections"),
    ("close", cmd_close, "Close connection"),
    ("session", cmd_session, "Show all session info"),
    ("login", cmd_login, "Login user or show current login"),
    ("logout", cmd_logout, "Logout user"),
    ("ls", cmd_ls, "List content of folder or service"),
    ("get", cmd_get, "Download XML or JSON source"),
    ("put", cmd_put, "Upload XML source or change file"),
    ("rm", cmd_rm, "Remove object"),
    ("show", cmd_show, "Show object"),
    ("mkdir", cmd_mkdir, "Create new folder"),
    ("undo", cmd_undo, "Undo last change"),
    ("vars", cmd_vars, "Set field variables"),
    ("call", cmd_call, "Invoke transaction or operation"),
    ("listen", cmd_listen, "Listen on a provision='rest' service"))


def get_version():
    """
    Returns the content of the version.txt compile-time file.
    """
    filepath = pkg_resources.resource_filename(
        __package__, "version.txt")
    version = "Unknown"
    with open(filepath, "r") as version_file:
        version = version_file.read().replace("\n", "")
    return __package__ + " " + version


def parse_args():
    """
    Returns the parsed command and command arguments.

    This calls out to each submodule to parse the command line
    arguments.
    """
    prog_name = os.environ.get("SPARKL_PROG_NAME")
    if not prog_name:
        prog_name = __package__

    epilog = "Use '{ProgName} <cmd> -h' for subcommand help".format(
        ProgName=prog_name)

    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="SPARKL command line utility.",
        epilog=epilog,
        version=get_version())

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

    for (cmd, submodule, help_text) in MODULES:
        subparser = subparsers.add_parser(
            cmd,
            description=submodule.command.__doc__,
            help=help_text,
            epilog="(Choose connection with toplevel option -a/--alias)")
        subparser.set_defaults(
            fun=submodule.command)
        submodule.parse_args(subparser)

    return parser.parse_args(
        namespace=get_args())


def main():
    """
    Main function parses arguments.

    If the --version arg is specified, shows version and returns.

    Otherwise, it parses arguments into the common namespace object,
    performs a garbage collection to clean outdated sessions,
    and finally dispatches the specified command.
    """
    args = parse_args()

    garbage_collect()

    try:
        args.fun()
        sys.exit(0)

    except cli_exception.CliException as exception:
        print(exception)
        sys.exit(1)


# Allow invocation using `python -m sparkl_cli.main`
if __name__ == "__main__":
    main()
