"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Delete command implementation.

This works by creating a change file that deletes the
specified object.
"""
from __future__ import print_function

import os

from sparkl_cli.cli_exception import (
    CliException)

from sparkl_cli.common import (
    get_args,
    sync_request)


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "object",
        type=str,
        help="object id or path")


def command():
    """
    Deletes the specified configuration object.
    """
    args = get_args()
    folder = os.path.dirname(args.object)
    name = os.path.basename(args.object)

    if not folder:
        folder = "/"

    change = "<change><delete name=\"{Name}\"/></change>".format(
        Name=name)

    response = sync_request(
        args.alias, "POST", "sse_cfg/change/" + folder,
        headers={
            "x-sparkl-transform": "gen_change",
            "Content-Type": "application/xml"},
        data=change)

    if not response:
        raise CliException(
            "Error deleting {Object}".format(
                Object=args.object))
