"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Undo command implementation.

This performs the HTTP DELETE request and indicates whether
the undo was successful.
"""
from __future__ import print_function

from sparkl_cli.common import (
    sync_request)


def parse_args(_):
    """
    Adds module-specific subcommand arguments.
    """
    return


def command(args):
    """
    Undoes the last configuration change. The undo stack
    is per-user, meaning you can undo a change made in a
    previous session.
    """
    response = sync_request(
        args.alias, "DELETE", "sse_cfg/change")

    if response:
        parent = response.json()["attr"]["parent"]
        print("Undone change in", parent)
    else:
        print("Cannot undo")
