"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Make directory command implementation.

This works by creating a change file that creates the
specified folder.
"""
from __future__ import print_function

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
        "parent",
        type=str,
        help="path or id of the parent, which must exist")

    subparser.add_argument(
        "name",
        type=str,
        help="new folder name")


def command():
    """
    Creates a new subfolder in the specified parent folder.
    """
    args = get_args()
    change = "<change><folder name=\"{Name}\"/></change>".format(
        Name=args.name)

    response = sync_request(
        args.alias, "POST", "sse_cfg/change/" + args.parent,
        headers={
            "x-sparkl-transform": "gen_change",
            "Content-Type": "application/xml"},
        data=change)

    if not response:
        raise CliException(
            "Error creating folder {Folder} in {Parent}".format(
                Folder=args.name,
                Parent=args.parent))
