"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Main module implementing CLI for managing running SPARKL nodes.

This must be invoked as a package, to allow the relative import
of the command files to work:

  python -m sparkl_cli

Client state between invocations is maintained in the filesystem.
"""
import argparse
import os
import shutil
import tempfile
import psutil

from . import cmd_accept

COMMANDS = {
    "accept": cmd_accept.command}

TEMP_SUBDIR = os.path.join(
    tempfile.gettempdir(),
    "sse_cli")


def get_args():
    """
    Returns the parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog=__package__,
        description="SPARKL command line utility.")

    parser.add_argument(
        "cmd",
        help="the command to execute")

    parser.add_argument(
        "args",
        metavar="arg",
        type=str,
        nargs="*",
        help="the arguments to the command")

    return parser.parse_args()


def get_working_dir():
    """
    Returns the working directory for this invocation, which will
    remain the same for each invocation from a given parent pid.

    The directory is created if necessary.
    """
    working_dir = os.path.join(
        TEMP_SUBDIR,
        str(os.getppid()))

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    return working_dir


def garbage_collect():
    """
    Performs a garbage collection of temp dirs not associated with
    a running process.
    """
    for working_dir in os.listdir(TEMP_SUBDIR):
        pid = int(working_dir)
        if not psutil.pid_exists(pid):
            obsolete_dir = os.path.join(
                TEMP_SUBDIR,
                working_dir)
            shutil.rmtree(obsolete_dir)


def main():
    """
    Main function performs a garbage collection of temp directories
    and then dispatches according to the command.
    """
    garbage_collect()

    working_dir = get_working_dir()
    args = get_args()

    print "Command is " + args.cmd
    print "Package is " + __package__
    print "Name is " + __name__
    print working_dir
    print args.args

    try:
        dispatch = COMMANDS[args.cmd]
        dispatch(args.args)
    except KeyError:
        print "Unrecognized command: " + args.cmd

if __name__ == "__main__":
    main()
