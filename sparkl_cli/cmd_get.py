"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Get source command implementation.
"""
from __future__ import print_function

import xml.dom.minidom
import json

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
        help="object path relative to root of logged in user")

    subparser.add_argument(
        "file",
        type=str,
        nargs="?",
        help="optional name of file to save output")

    subparser.add_argument(
        "-f", "--format",
        type=str,
        default="xml",
        help="xml (default) or json")

    subparser.add_argument(
        "-p", "--pretty",
        action="store_true",
        help="pretty print output")


def prettify(output):
    """
    Returns the pretty-print version of the output,
    either XML or JSON according to the args.
    """
    args = get_args()
    if args.format.lower() == "xml":
        parsed = xml.dom.minidom.parseString(output)
        pretty = parsed.toprettyxml()

    else:
        parsed = json.loads(output)
        pretty = json.dumps(
            parsed, indent=4, sort_keys=True)

    return pretty


def save(output):
    """
    Saves the output text to the specified file.
    """
    args = get_args()
    filename = args.file
    with open(filename, "w") as output_file:
        output_file.write(output)


def command():
    """
    Lists the contents of the specified folder.
    """
    args = get_args()

    response = sync_request(
        args.alias, "GET", "sse_cfg/source/" + args.object,
        accept=args.format)

    if response:
        output = response.text
        if args.pretty:
            output = prettify(output)

        if args.file:
            save(output)
        else:
            print(output)
    else:
        raise CliException(
            "Cannot get {Object}".format(
                Object=args.object))
