"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Open command implementation.
"""

import os
import sys
import requests

from sparkl_cli.common import (
    get_state, set_state)


def show_connections():
    """
    Shows open connections, if any.
    """
    state = get_state()
    connections = state.get("connections", {})
    current = state.get("current_connection", None)
    count = len(connections)

    if count > 0:
        for alias in connections:
            if alias == current:
                print "*",

            connection = connections[alias]
            print "{Alias}: {HostUrl}".format(
                Alias=alias,
                HostUrl=connection["host_url"])
    else:
        print "No open connections"


def open_connection(alias):
    """
    Makes the existing connection specified by alias current.

    If the connection is valid, prints the connection info.

    If the connection is invalid, removes it from the state.
    """
    state = get_state()
    connections = state.get("connections", {})
    connection = connections.get(alias, None)

    if not connection:
        print "error: no connection {Alias}".format(
            Alias=alias)
        sys.exit(1)

    host_url = connection.get("host_url")
    request_url = os.path.join(
        host_url, "sse/ping")

    try:
        response = requests.get(
            request_url,
            headers={
                "Accept": "application/json"})

        if response.status_code != 200:
            raise ValueError("Received error response")

        state["current_connection"] = alias
        set_state(state)

        print "current: " + alias
        print "url: " + host_url
        attrs = response.json()["attr"]
        for key in attrs:
            print key + ": " + attrs[key]

    except BaseException:
        connections.pop(alias, None)
        state["connections"] = connections
        state.pop("current_connection", None)
        set_state(state)
        print "No SPARKL at " + host_url
        sys.exit(1)


def new_connection(alias, host_url):
    """
    Opens a new connection with the specified alias to the host url,
    making it the current open connection.

    Prints the ping info if connection is valid.
    Prints an error if the connection cannot be opened.
    """
    state = get_state()
    connections = state.get("connections", {})

    if alias in state["connections"]:
        print "error: {Alias} already open".format(
            Alias=alias)
        sys.exit(1)

    connection = {
        "host_url": host_url}
    connections[alias] = connection
    state["connections"] = connections
    set_state(state)
    open_connection(alias)


def command(args):
    """
    Opens a new connection and makes it current, or makes an existing
    connection current, or shows existing connections.
    """
    argc = len(args)
    if argc == 0:
        show_connections()
    elif argc == 1:
        alias = args[0]
        open_connection(alias)
    elif argc == 2:
        alias = args[0]
        host_url = args[1]
        new_connection(alias, host_url)
    else:
        print "Usage: open [<alias> [<host_url>]]"
        sys.exit(1)
