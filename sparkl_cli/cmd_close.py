"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Close command implementation.
"""
from __future__ import print_function

from sparkl_cli.common import (
    get_state,
    set_state,
    delete_cookies)


def parse_args(_):
    """
    Adds the module-specific subcommand arguments.
    """
    return


def command(args):
    """
    Closes the connection with the given alias, if already open.
    """
    alias = args.alias

    state = get_state()
    connections = state.get("connections", {})

    if connections.get(alias):
        delete_cookies(alias)
        connections.pop(alias)
        set_state(state)
    else:
        print("No such connection:", alias)
