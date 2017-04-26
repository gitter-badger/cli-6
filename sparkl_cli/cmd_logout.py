"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Logout command implementation.
"""
from __future__ import print_function

from sparkl_cli.common import (
    sync_request)

DESCRIPTION = "Logs out current user"


def parse_args(_):
    """
    Adds module-specific subcommand arguments.
    """
    return


def logout(args):
    """
    Logs out the user, if already logged in.
    """
    response = sync_request(
        args.alias, "POST", "sse_cfg/signout")

    if not response:
        print("Logout failed")


def command(args):
    """
    Logs out the currently logged-in user, if any.
    """
    logout(args)
