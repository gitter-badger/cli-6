"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Close command implementation.
"""
from __future__ import print_function

from sparkl_cli.cli_exception import (
    CliException)

from sparkl_cli.common import (
    get_state,
    set_state,
    delete_cookies)

from . import common


def parse_args(_):
    """
    Adds the module-specific subcommand arguments.
    """
    return


def command():
    """
    Closes the connection with the given alias, if already open.
    """
    args = common.ARGS

    state = get_state()
    connections = state.get("connections", {})

    if connections.get(args.alias):
        delete_cookies(args.alias)
        connections.pop(args.alias)
        set_state(state)
    else:
        raise CliException(
            "No connection alias {Alias}".format(
                Alias=args.alias))
