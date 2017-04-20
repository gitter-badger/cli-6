"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Utility module for common functions.
"""
import argparse
import os
import shutil
import tempfile
import psutil


def working_root():
    """
    Returns the working root under which a working directory
    is created for each process invoking the cli.
    """
    return os.path.join(
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
        working_root(),
        str(os.getppid()))

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    return working_dir


def garbage_collect():
    """
    Performs a garbage collection of temp dirs not associated with
    a running process.
    """
    for working_dir in os.listdir(working_root()):
        pid = int(working_dir)
        if not psutil.pid_exists(pid):
            obsolete_dir = os.path.join(
                working_root(),
                working_dir)
            shutil.rmtree(obsolete_dir)
