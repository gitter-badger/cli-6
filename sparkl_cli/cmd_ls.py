"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

List command implementation.
"""
from __future__ import print_function

from sparkl_cli.common import (
    sync_request)

DESCRIPTION = "Lists content of specified folder"


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "folder",
        type=str,
        nargs="?",
        default="/",
        help="folder id or path")


def list_folder(args):
    """
    Lists the content of the folder specified in the args.
    """
    response = sync_request(
        args.alias, "GET", "sse_cfg/content/" + args.folder)

    if response:
        if "content" in response.json():
            content = response.json()["content"]
            for entry in content:
                print(
                    entry["tag"],
                    entry["attr"]["id"],
                    entry["attr"].get("name", ""),
                    sep="\t")
        else:
            print("No content")
    else:
        print("Cannot list folder", args.folder)


def command(args):
    """
    Lists the contents of the specified folder.
    """
    list_folder(args)
