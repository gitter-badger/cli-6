"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Get source command implementation.
"""
from __future__ import print_function

import xml.dom.minidom
import json

from sparkl_cli.common import (
    sync_request)

DESCRIPTION = "Gets the (deep) source of the specified object"


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "object",
        type=str,
        help="object path relative to root of logged in user")

    subparser.add_argument(
        "-f", "--format",
        type=str,
        default="xml",
        help="xml (default) or json")

    subparser.add_argument(
        "-p", "--pretty",
        action="store_true",
        help="pretty print output")

    subparser.add_argument(
        "-o", "--output",
        type=str,
        help="save output in file OUTPUT")


def prettify(args, output):
    """
    Returns the pretty-print version of the output,
    either XML or JSON according to the args.
    """
    if args.format.lower() == "xml":
        parsed = xml.dom.minidom.parseString(output)
        pretty = parsed.toprettyxml()

    else:
        parsed = json.loads(output)
        pretty = json.dumps(
            parsed, indent=4, sort_keys=True)

    return pretty


def save(filename, output):
    """
    Saves the output text to the specified file.
    """
    with open(filename, "w") as output_file:
        output_file.write(output)


def command(args):
    """
    Lists the contents of the specified folder.
    """
    response = sync_request(
        args.alias, "GET", "sse_cfg/source/" + args.object,
        accept=args.format)

    if response:
        output = response.text
        if args.pretty:
            output = prettify(args, output)

        if args.output:
            save(args.output, output)
        else:
            print(output)
    else:
        print("Cannot get object", args.object)
