"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Utility module for common functions.
"""
from __future__ import print_function

import os
import shutil
import tempfile
import json
import urlparse
import cookielib
import requests
import psutil

STATE_FILE = "state.json"
DEFAULT_TIMEOUT = 3

# Set by main module.
SESSION_PID = None
ALIAS = None


def get_working_root():
    """
    Returns the working root under which a working directory
    is created for each process invoking the cli.

    Creates the working root if not already present.
    """
    working_root = os.path.join(
        tempfile.gettempdir(),
        "sse_cli")

    if not os.path.exists(working_root):
        os.makedirs(working_root)

    return working_root


def get_working_dir():
    """
    Returns the working directory for this invocation, using the
    common session id.

    The directory is created if necessary.
    """

    working_dir = os.path.join(
        get_working_root(),
        str(SESSION_PID))

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    return working_dir


def garbage_collect():
    """
    Performs a garbage collection of temp dirs not associated with
    a running process.
    """
    for working_dir in os.listdir(get_working_root()):
        pid = int(working_dir)
        if not psutil.pid_exists(pid):
            obsolete_dir = os.path.join(
                get_working_root(),
                working_dir)
            shutil.rmtree(obsolete_dir)


def get_state():
    """
    Gets the current state dictionary, or empty dictionary
    if none.
    """
    name = os.path.join(
        get_working_dir(), STATE_FILE)

    if os.path.isfile(name):
        with open(name, "r") as state_file:
            state = json.load(state_file)
    else:
        state = {}

    return state


def set_state(state):
    """
    Saves the new state dictionary.
    """
    name = os.path.join(
        get_working_dir(), STATE_FILE)

    with open(name, "w") as state_file:
        json.dump(state, state_file)


def get_connection(alias):
    """
    Gets the specified connection from the state object.

    Throws an exception if no such connection alias exists.
    """
    state = get_state()
    connections = state.get("connections", {})
    return connections[alias]


def put_connection(alias, connection):
    """
    Puts the connection dict into the state object under the
    given alias name.
    """
    state = get_state()
    connections = state.get("connections", {})
    connections[alias] = connection
    set_state(state)


def get_cookie_jar(alias):
    """
    Gets the cookie jar for the given alias, creating it
    if necessary.
    """
    cookie_file = os.path.join(
        get_working_dir(), alias + ".cookies")
    cookie_jar = cookielib.LWPCookieJar(cookie_file)
    try:
        cookie_jar.load()
    except BaseException:
        # Cookie file doesn't exist yet.
        pass

    return cookie_jar


def del_cookie_jar(alias):
    """
    Deletes the cookie jar for the given alias.
    """
    cookie_file = os.path.join(
        get_working_dir(), alias + ".cookies")
    os.remove(cookie_file)


def sync_request(
        alias, method, href,
        params=None,
        data=None,
        accept="json",
        timeout=DEFAULT_TIMEOUT):
    """
    Makes a request on the specified connection, using
    the connection session state including session cookies.

    Method can be 'GET' or 'POST' upper or lower case.
    Href is relative to the base url, e.g. 'sse_cfg/user'.
    Params is a dict, or None.
    Body is a string, or None, used in POST request only.

    Returns a response object, or None if an HTTP request
    exception occurred.
    """
    connection = get_connection(alias)
    cookies = get_cookie_jar(alias)
    base = connection.get("url")
    request_url = urlparse.urljoin(base, href)
    headers = {
        "Accept": "application/" + accept}

    try:
        if method.upper() == "GET":
            response = requests.get(
                request_url,
                headers=headers,
                params=params,
                timeout=timeout,
                cookies=cookies)
            cookies.save(ignore_discard=True)
            return response

        if method.upper() == "POST":
            response = requests.post(
                request_url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
                cookies=cookies)
            cookies.save(ignore_discard=True)
            return response

        return None

    except BaseException as exception:
        print(exception)
        return None
