"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <yev@sparkl.com> Yevheniy Vlasenko.

Provides the CliWebsocket class used to handle JSON websocket events.
"""
from __future__ import print_function

import json
import logging
import websocket

from sparkl_cli.cli_exception import (
    CliException)

from sparkl_cli.common import (
    unpickle_cookies)

from . import common


class CliWebsocket(object):
    """
    Websocket class opens a connection using the session cookie
    to allow access to REST services.

    It then receives JSON messages and invokes the on_message
    callback function.
    """

    def __init__(self, ws_url):
        """
        Opens the websocket url.
        """
        self.ws_url = ws_url
        self.on_message = lambda name, data: None
        cookies = unpickle_cookies(common.ARGS.alias)
        session = cookies["ipaas_session"]

        self.ws_connection = websocket.WebSocketApp(
            ws_url,
            on_message=self.__ws_message,
            on_error=self.__ws_error,
            on_close=self.__ws_close,
            cookie="ipaas_session=" + session)

        self.ws_connection.on_open = self.__ws_open
        logging.basicConfig()

    def __ws_error(self, ws_connection, error):
        """
        Callback on websocket error.
        """
        print("error", ws_connection, error)
        raise CliException(
            "Websocket error on {WsUrl}".format(
                WsUrl=self.ws_url))

    def __ws_open(self, _ws_connection):
        """
        Callback on websocket open.
        """
        print("Websocket opened on {WsUrl}".format(
            WsUrl=self.ws_url))

    def __ws_close(self, _ws_connection):
        """
        Callback on websocket close.
        """
        print("Websocket closed on {WsUrl}".format(
            WsUrl=self.ws_url))

    def __ws_message(self, _ws_connection, message):
        """
        Callback on websocket message. This is assumed
        to be JSON in the form provided by the svc_rest
        service.

        This means that "call" holds the operation name,
        and "data" holds a dict of field values keyed by
        field name.
        """
        message_object = json.loads(message)
        name = message_object["call"]
        data = message_object["data"]

        if hasattr(self, 'on_message'):
            self.on_message(name, data)

    def open(self):
        """
        User method to open this websocket.
        """
        print(self.ws_url)
        self.ws_connection.run_forever()

    def close(self):
        """
        User method to close this websocket.
        """
        pass
