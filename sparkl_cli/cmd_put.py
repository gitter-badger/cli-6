"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Upload source command implementation.
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
        "file",
        type=str,
        help="file name containing XML to upload")

    subparser.add_argument(
        "folder",
        type=str,
        help="folder id or path, into which the change is placed")


def command():
    """
    Uploads SPARKL source or other valid XML change file.
    """
    args = get_args()
    with open(args.file, "rb") as upload_file:
        response = sync_request(
            args.alias, "POST", "sse_cfg/change/" + args.folder,
            headers={
                "x-sparkl-transform": "gen_change",
                "Content-Type": "application/xml"},
            data=upload_file)

    if not response:
        raise CliException(
            "Error uploading {File} to {Folder}".format(
                File=args.file,
                Folder=args.folder))
