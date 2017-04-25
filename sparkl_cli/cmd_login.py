"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Login command implementation.
"""
from __future__ import print_function

import sys
import posixpath
import getpass
import requests

from sparkl_cli.common import (
    assert_current_connection,
    put_connection)

DESCRIPTION = "Logs in the specified user with password"


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "user",
        nargs="?",
        type=str,
        help="email of user to be logged in.")
    subparser.add_argument(
        "password",
        nargs="?",
        type=str,
        help="password of user. Omit to be prompted.")


def show_login():
    """
    Shows the logged in user, if any, on the currently open connection.
    """
    (alias, connection) = assert_current_connection()
    user = connection.get("user", None)
    if user:
        print(alias + ": " + user)
    else:
        print("No user logged in to", alias)


def login(email, password):
    """
    Logs in the specified user using the password.
    """
    (alias, connection) = assert_current_connection()
    user = connection.get("user", None)
    if user:
        print("User already logged in:", user)
        sys.exit(1)

    host_url = connection.get("host_url")
    post_url = posixpath.join(
        host_url, "sse_cfg/user")

    try:
        response = requests.post(
            post_url,
            data={
                "email": email,
                "password": password})

        if response.status_code != 200:
            raise ValueError("Received error response")

        connection["user"] = email
        put_connection(alias, connection)

    except BaseException:
        print("Failed to login:", email)
        sys.exit(1)


def command(args):
    """
    Logs in the named user, prompting for password if not provided.
    """
    if not args.user:
        show_login()
    elif not args.password:
        password = getpass.getpass("Password: ")
        login(args.user, password)
    else:
        login(args.user, args.password)
