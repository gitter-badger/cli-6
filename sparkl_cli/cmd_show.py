"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Show object command implementation.
"""
from __future__ import print_function

from sparkl_cli.common import (
    sync_request,
    show_struct)

DESCRIPTION = "Shows detail about the specified object"


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "object",
        type=str,
        help="object id or path")


def command(args):
    """
    Shows the object specified in the args.
    """
    response = sync_request(
        args.alias, "GET", "sse_cfg/object/" + args.object)

    if response:
        show_struct(response.json())
    else:
        print("Cannot show", args.object)
