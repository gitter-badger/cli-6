"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Close command implementation.
"""
from __future__ import print_function

import sys

from sparkl_cli.common import (
    get_state, set_state)

DESCRIPTION = "Closes the named connection"


def parse_args(subparser):
    """
    Adds the module-specific subcommand arguments.
    """
    subparser.add_argument(
        "alias",
        type=str,
        help="short name of the connection to be closed")


def command(args):
    """
    Closes the connection with the given alias, if already open.
    """
    alias = args.alias

    state = get_state()
    connections = state.get("connections", {})

    if connections.get(alias):
        connections.pop(alias)
        state["connections"] = connections

        if state.get("current_connection", None) == alias:
            state.pop("current_connection")

        set_state(state)
    else:
        print("No such connection:", alias)
        sys.exit(1)
