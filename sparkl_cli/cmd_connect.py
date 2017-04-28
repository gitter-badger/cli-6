"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Open command implementation.
"""
from __future__ import print_function

from sparkl_cli.common import (
    get_state,
    set_state,
    sync_request,
    show_struct)


def parse_args(subparser):
    """
    Module-specific subcommand arguments.
    """
    subparser.add_argument(
        "url",
        nargs="?",
        type=str,
        help="URL of a SPARKL node, e.g. http://localhost:8000")


def show_connections():
    """
    Shows connections, if any.
    """
    state = get_state()
    connections = state.get("connections", {})
    count = len(connections)

    if count > 0:
        for alias in connections:
            connection = connections[alias]
            url = connection["url"]
            print(alias, url)
    else:
        print("No connections")


def new_connection(args):
    """
    Opens a new connection with the specified alias to the host url,
    unless there is already a connection with that alias.

    Prints the ping info if connection is valid.
    Prints an error if the connection cannot be opened. This will cause
    there to be no current connection.
    """
    state = get_state()
    connections = state.get("connections", {})

    if args.alias in connections:
        print(args.alias, "already open")
        return

    connection = {
        "url": args.url}
    connections[args.alias] = connection
    state["connections"] = connections
    set_state(state)

    response = sync_request(
        args.alias, "GET", "sse/ping")

    if response:
        show_struct(response.json())

    else:
        connections.pop(args.alias, None)
        set_state(state)
        print("No SPARKL at", args.url)


def command(args):
    """
    Opens a new connection if url is specified, otherwise shows
    existing connections if any.
    """
    if args.url:
        new_connection(args)
    else:
        show_connections()
