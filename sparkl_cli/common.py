"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Utility module for common functions.
"""
import argparse
import os
import shutil
import tempfile
import json
import psutil

STATE_FILE = "state.json"


def get_working_root():
    """
    Returns the working root under which a working directory
    is created for each process invoking the cli.

    Creates the working root if not already present.
    """
    working_root = os.path.join(
        tempfile.gettempdir(),
        "sse_cli")

    if not os.path.exists(working_root):
        os.makedirs(working_root)

    return working_root


def get_args():
    """
    Returns the parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog=__package__,
        description="SPARKL command line utility.")

    parser.add_argument(
        "-o", "--owner",
        type=int,
        default=os.getppid(),
        help="optional session owner pid")

    parser.add_argument(
        "cmd",
        help="the command to execute")

    parser.add_argument(
        "cmd_args",
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
        get_working_root(),
        str(os.getppid()))

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    return working_dir


def garbage_collect():
    """
    Performs a garbage collection of temp dirs not associated with
    a running process.
    """
    for working_dir in os.listdir(get_working_root()):
        pid = int(working_dir)
        if not psutil.pid_exists(pid):
            obsolete_dir = os.path.join(
                get_working_root(),
                working_dir)
            shutil.rmtree(obsolete_dir)


def get_state():
    """
    Gets the current state dictionary, or empty dictionary
    if none.
    """
    name = os.path.join(
        get_working_dir(), STATE_FILE)

    if os.path.isfile(name):
        with open(name, "r") as state_file:
            state = json.load(state_file)
    else:
        state = {}

    return state


def set_state(state):
    """
    Saves the new state dictionary.
    """
    name = os.path.join(
        get_working_dir(), STATE_FILE)

    with open(name, "w") as state_file:
        json.dump(state, state_file)
