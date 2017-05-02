"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Login command implementation.
"""
from __future__ import print_function

import getpass

from sparkl_cli.cli_exception import (
    CliException)

from sparkl_cli.common import (
    sync_request)

from . import common


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
    Shows the logged in user on the connection specified in
    the args, or default.
    """
    args = common.ARGS
    response = sync_request(
        args.alias, "GET", "sse_cfg/user")

    if response:
        print("alias", args.alias)
        attrs = response.json()["attr"]
        for key in attrs:
            print(key, attrs[key])


def login():
    """
    Logs in the specified user, prompting for password
    if necessary.
    """
    args = common.ARGS
    if not args.password:
        args.password = getpass.getpass("Password: ")

    response = sync_request(
        args.alias, "POST", "sse_cfg/user",
        data={
            "email": args.user,
            "password": args.password})

    if not response:
        raise CliException(
            "Failed to login {User}".format(
                User=args.user))


def register():
    """
    Registers the specified user, prompting twice for
    password if necessary.
    """
    args = common.ARGS
    if not args.password:
        args.password = getpass.getpass("Password: ")
        check = getpass.getpass("Repeat: ")
        if args.password != check:
            raise CliException(
                "Passwords do not match")

    response = sync_request(
        args.alias, "POST", "sse_cfg/register",
        data={
            "email": args.user,
            "password": args.password})

    if not response:
        raise CliException(
            "Failed to register {User}".format(
                User=args.user))


def command():
    """
    Logs in or registers the user. If no user specified, shows
    the current login status.
    """
    args = common.ARGS
    if not args.user:
        show_login()
    elif args.register:
        register()
    else:
        login()
