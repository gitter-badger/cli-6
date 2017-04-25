"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Logout command implementation.
"""
from __future__ import print_function

import sys
import posixpath
import requests

from sparkl_cli.common import (
    assert_current_connection,
    put_connection)

DESCRIPTION = "Logs out user on current connection"


def parse_args(_):
    """
    Adds module-specific subcommand arguments.
    """
    return


def logout():
    """
    Logs out the user, if already logged in.
    """
    (alias, connection) = assert_current_connection()
    user = connection.get("user", None)
    if not user:
        print("No user logged in to", alias)
        sys.exit(1)

    host_url = connection.get("host_url")
    post_url = posixpath.join(
        host_url, "sse_cfg/signout")

    try:
        response = requests.post(
            post_url)

        if response.status_code != 200:
            raise ValueError("Received error response")

        connection.pop("user", None)
        put_connection(alias, connection)

    except BaseException:
        print("Failed to logout")
        sys.exit(1)


def command(_):
    """
    Logs out the currently logged-in user, if any.
    """
    logout()
