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
    get_args,
    get_connection)

from . import common


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "-c", "--consume",
        type=str,
        default="Log",
        help="Show events from the named consume operation only [Log]")

    subparser.add_argument(
        "-f", "--field",
        type=str,
        default="event",
        help="Show value of the named field only [event]")

    subparser.add_argument(
        "service",
        type=str,
        nargs="?",
        default="Scratch/TraceLogger",
        help="Path or id of trace service [Scratch/TraceLogger]")


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

    If the -c or -f options are selected, filters the output appropriately.
    """
    args = get_args()

    if args.consume and name != args.consume:
        return

    if args.field:
        value = data.get(args.field)
        if value:
            print(value, "", sep="\n")
        return

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
    Opens a websocket listening to consume operations on the specified REST
    service.

    You can optionally filter out all but one consume operation and all but one
    field, using the -c and -f arguments respectively.

    The default values of the REST service, the consume operation filter and
    the field filter are set to "Scratch/Tracelogger", "Log" and "event"
    respectively, since these are default entries in the user configuration
    tree.
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
