"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Close command implementation.
"""

from sparkl_cli.common import (
    get_state, set_state)


def command(args):
    """
    Closes the connection with the given alias, if already open.
    """
    alias = args[0]

    state = get_state()
    connections = state.get("connections", {})

    if connections.get(alias):
        connections.pop(alias)
        state["connections"] = connections

        if state.get("current_connection", None) == alias:
            state.pop("current_connection")

        set_state(state)
