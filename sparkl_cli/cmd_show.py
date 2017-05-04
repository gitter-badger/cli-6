"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Show object command implementation.
"""
from __future__ import print_function

from sparkl_cli.cli_exception import (
    CliException)

from sparkl_cli.common import (
    get_args,
    get_object,
    show_struct)


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
    Shows detail about the specified object.
    """
    args = get_args()
    sparkl_object = get_object(args.alias, args.object)
    if sparkl_object:
        show_struct(sparkl_object)
    else:
        raise CliException(
            "Cannot show object {Object}".format(
                Object=args.object))
