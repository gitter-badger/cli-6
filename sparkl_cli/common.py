"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Utility module for common functions.
"""
import os
import shutil
import tempfile
import json
import sys
import psutil

STATE_FILE = "state.json"
SESSION_PID = None


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


def get_working_dir():
    """
    Returns the working directory for this invocation, using the
    common session id.

    The directory is created if necessary.
    """

    working_dir = os.path.join(
        get_working_root(),
        str(SESSION_PID))

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


def assert_current_connection():
    """
    Returns a tuple of the current alias name and the associated
    connection dict.

    If no connection is current, exits with an error.
    """
    state = get_state()
    current = state.get("current_connection", None)
    if not current:
        print "No current connection"
        sys.exit(1)

    connections = state.get("connections", {})
    connection = connections.get(current)
    return (current, connection)


def put_connection(alias, connection):
    """
    Puts the connection dict into the state object under the
    given alias name.
    """
    state = get_state()
    connections = state.get("connections", {})
    connections[alias] = connection
    state["connections"] = connections
    set_state(state)
