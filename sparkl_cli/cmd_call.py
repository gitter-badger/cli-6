"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Invoke operation command implementation.
"""
from __future__ import print_function


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "operation",
        help="operation path or id")


def command(_):
    """
    Invoked the named operation using the previously set field values.
    In the case of a solicit or notify, this causes a transaction to
    be executed.
    In the case of a request or consume, the individual operation
    is executed.
    """
    return
