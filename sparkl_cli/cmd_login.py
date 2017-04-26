"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Login command implementation.
"""
from __future__ import print_function

import getpass

from sparkl_cli.common import (
    sync_request)

DESCRIPTION = """\
    Logs in, or registers, the specified user with password.
    If no user is given, returns the current login information.
    """


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


def show_login(args):
    """
    Shows the logged in user on the connection specified in
    the args, or default.
    """
    response = sync_request(
        args.alias, "GET", "sse_cfg/user")

    if response:
        print("alias", args.alias)
        attrs = response.json()["attr"]
        for key in attrs:
            print(key, attrs[key])
    else:
        print("Connection error on", args.alias)


def login(args):
    """
    Logs in the specified user, prompting for password
    if necessary.
    """
    if not args.password:
        args.password = getpass.getpass("Password: ")

    response = sync_request(
        args.alias, "POST", "sse_cfg/user",
        data={
            "email": args.user,
            "password": args.password})

    if not response:
        print("Login failed")


def register(args):
    """
    Registers the specified user, prompting twice for
    password if necessary.
    """
    if not args.password:
        args.password = getpass.getpass("Password: ")
        check = getpass.getpass("Repeat: ")
        if args.password != check:
            print("Passwords do not match")
            return

    response = sync_request(
        args.alias, "POST", "sse_cfg/register",
        data={
            "email": args.user,
            "password": args.password})

    if not response:
        print("Register user failed")


def command(args):
    """
    Logs in or registers the user. If no user specified, shows
    the current login status.
    """
    if not args.user:
        show_login(args)
    elif args.register:
        register(args)
    else:
        login(args)
