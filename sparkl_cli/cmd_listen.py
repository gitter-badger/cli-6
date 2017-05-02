"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Listen command implementation.
"""
from __future__ import print_function

from urlparse import (
    urlsplit,
    urlunsplit)

from sparkl_cli.cli_exception import (
    CliException)

from sparkl_cli.cli_websocket import (
    CliWebsocket)

from sparkl_cli.common import (
    get_connection)

from . import common


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "service",
        type=str,
        nargs="?",
        default="Scratch/TraceLogger",
        help="Path or id of trace service, default 'Scratch/TraceLogger'")


def get_cli_ws():
    """
    Returns the opened CliWebsocket instance on the specified REST service.
    """
    args = common.ARGS
    connection = get_connection(args.alias)
    http_url = connection.get("url")
    (scheme, netloc, _path, _query, _frag) = urlsplit(http_url)

    if scheme == "http":
        ws_scheme = "ws"
    else:
        ws_scheme = "wss"

    ws_path = "svc_rest/websocket/" + args.service

    ws_url = urlunsplit((ws_scheme, netloc, ws_path, "", ""))

    cli_ws = CliWebsocket(ws_url)
    return cli_ws


def on_message(name, data):
    """
    Callback registered on the CliWebsocket instance.

    This is invoked for each message, with the name of the operation (e.g.
    the Log operation) and a dict of data fields keyed by name.

    If there is one field, it is
    """
    for key in data:
        value = data[key]
        print("{Name}[{Key}]".format(
            Name=name,
            Key=key), value, "", sep="\n")


def listen(cli_ws):
    """
    Lists the content of the folder specified in the args.
    """
    cli_ws.on_message = on_message
    cli_ws.open()


def command():
    """
    Opens a websocket listening to the specified REST service, most commonly
    a tracelogger.

    A tracelogger service has a single consume operation on it, where the
    consume has the 'sse.log' property which marks it out as a log operation.

    It normally has a single input field whose name is generally 'event'.

    The raw events are dumped to the standard output.
    """
    args = common.ARGS
    service = common.get_object(args.alias, args.service)
    if not service:
        raise CliException(
            "No service {Service}".format(
                Service=args.service))

    provision = service["attr"]["provision"]
    if provision != "rest":
        raise CliException(
            "Service provision='{Provision}', should be 'rest'".format(
                Provision=provision))

    cli_ws = get_cli_ws()
    listen(cli_ws)
