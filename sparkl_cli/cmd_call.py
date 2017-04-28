"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Invoke operation command implementation.

This uses the sse_svc_dispatcher API, which requires that
we construct the event and data client-side.

It would be very much easier to change sse_svc_dispatcher to
use named fields!
"""
from __future__ import print_function

import os
import json

from sparkl_cli.common import (
    get_object,
    sync_request,
    show_struct)

from sparkl_cli.cmd_vars import (
    get_vars)


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "operation",
        help="operation path or id")


def sparkl_type(field_type, string_value):
    """
    Uses the field type to coerce the string value to the
    json-compatible python equivalent. Binary and term are
    left as string.
    """
    value = string_value
    if field_type == "integer":
        value = int(string_value)
    elif field_type == "boolean":
        value = bool(string_value)
    elif field_type == "float":
        value = float(string_value)
    return value


def to_datum(field_id, field_name, field_type, field_value):
    """
    Returns the datum formed from the field data.

    Prints a message and returns None if there is no field value,
    or the "read" method cannot populate the value.
    """
    if not field_value:
        print("Missing var", field_name, field_type)
        return None

    [method, string_value] = field_value

    if method == "read":
        if os.path.isfile(string_value):
            with open(string_value, "r") as value_file:
                string_value = value_file.read()
        else:
            print("Missing file", string_value, "for var", field_name)
            return None

    value = sparkl_type(field_type, string_value)

    datum = {
        "tag": "datum",
        "attr": {
            "field": field_id
        },
        "content": [value]}
    return datum


def command(args):
    """
    Invoked the named operation. Existing vars are used to populate
    the field values, where needed.
    In the case of a solicit or notify, this causes a transaction to
    be executed.
    In the case of a request or consume, the individual operation
    is executed.
    """
    operation = get_object(args.alias, args.operation)
    if not operation:
        print("No operation", args.operation)
        return

    vars_dict = get_vars()
    data = []
    can_dispatch = True
    tag = operation["tag"]
    subject = operation["attr"]["id"]

    for field_id in operation["attr"]["fields"].split():
        field = get_object(args.alias, field_id)
        field_type = field["attr"]["type"]
        if field_type:
            field_name = field["attr"]["name"]
            field_value = vars_dict.get(field_name, None)
            datum = to_datum(
                field_id, field_name, field_type, field_value)
            if datum:
                data.append(datum)
            else:
                can_dispatch = False

    if not can_dispatch:
        print("Cannot dispatch", tag)
        return

    data_event = json.dumps({
        "tag": "data_event",
        "attr": {
            "subject": subject
        },
        "content": data})

    response = sync_request(
        args.alias, "POST", "sse_svc_dispatcher/" + tag,
        headers={
            "Content-Type": "application/json"},
        data=data_event)

    if not response:
        print("Error dispatching")
        return

    show_struct(response.json())
