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

DESCRIPTION = "Logs in, or registers, the specified user with password."


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "-r", "--register",
        action="store_true",
        help="register the user, creating if necessary")
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
        print(alias, user)
    else:
        print("No user logged in to", alias)


def login(args):
    """
    Logs in the specified user, prompting for password
    if necessary.
    """
    (alias, connection) = assert_current_connection()
    user = connection.get("user", None)
    if user:
        print("User already logged in:", user)
        sys.exit(1)

    user = args.user
    password = args.password

    if not password:
        password = getpass.getpass("Password: ")

    host_url = connection.get("host_url")
    post_url = posixpath.join(
        host_url, "sse_cfg/user")

    try:
        response = requests.post(
            post_url,
            data={
                "email": user,
                "password": password})

        if response.status_code != 200:
            raise ValueError("Received error response")

        connection["user"] = user
        put_connection(alias, connection)

    except BaseException:
        print("Failed to login:", user)
        sys.exit(1)


def register(args):
    """
    Registers the specified user, prompting twice for
    password if necessary.
    """
    (alias, connection) = assert_current_connection()
    user = connection.get("user", None)
    if user:
        print("User already logged in:", user)
        sys.exit(1)

    user = args.user
    password = args.password

    if not password:
        password = getpass.getpass("Password: ")
        check = getpass.getpass("Repeat: ")
        if password != check:
            print("Passwords do not match")
            sys.exit(1)

    host_url = connection.get("host_url")
    post_url = posixpath.join(
        host_url, "sse_cfg/register")

    try:
        response = requests.post(
            post_url,
            data={
                "email": user,
                "password": password})

        if response.status_code != 200:
            raise ValueError("Received error response")

        connection["user"] = user
        put_connection(alias, connection)

    except BaseException:
        print("Failed to register:", user)
        sys.exit(1)


def command(args):
    """
    Logs in or registers the user. If no user specified, shows
    the current login status.
    """
    if not args.user:
        show_login()
    elif args.register:
        register(args)
    else:
        login(args)
