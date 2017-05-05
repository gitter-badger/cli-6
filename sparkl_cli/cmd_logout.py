"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Logout command implementation.
"""
from __future__ import print_function

from sparkl_cli.common import (
    get_args,
    sync_request)


def parse_args(_):
    """
    Adds module-specific subcommand arguments.
    """
    return


def logout():
    """
    Logs out the user, if already logged in.
    """
    args = get_args()
    sync_request(
        args.alias, "POST", "sse_cfg/signout")


def command():
    """
    Logs out the currently logged-in user, if any.
    """
    logout()
