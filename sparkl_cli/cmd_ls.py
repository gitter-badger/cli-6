"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

List command implementation.
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
        "folder",
        type=str,
        nargs="?",
        default="/",
        help="folder id or path")


def list_folder():
    """
    Lists the content of the folder specified in the args.
    """
    args = get_args()
    response = sync_request(
        args.alias, "GET", "sse_cfg/content/" + args.folder)

    if not response:
        raise CliException(
            "Cannot list content of {Folder}".format(
                Folder=args.folder))

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


def command():
    """
    Lists the contents of the specified folder. Each line
    shows the type, id and name of a folder entry; or the
    type and id of a service instance.
    """
    list_folder()
