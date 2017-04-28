"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Set var command implementation.

Each entry in the vars dict is keyed by name. The value is a
tuple comprising ('literal', value) or ('read', value), where
the latter refers to a file containing the value.
"""
from __future__ import print_function

from sparkl_cli.common import (
    get_state,
    set_state)


def parse_args(subparser):
    """
    Adds module-specific subcommand arguments.
    """
    subparser.add_argument(
        "-c", "--clear",
        action="store_true",
        help="clear all vars (before any are set)")

    subparser.add_argument(
        "-l", "--literal",
        nargs=2,
        metavar=("name", "value"),
        action="append",
        help="literal value (e.g. -l age 35)")

    subparser.add_argument(
        "-r", "--read",
        nargs=2,
        metavar=("name", "filename"),
        action="append",
        help="read value from filename (e.g. -r contract file.pdf)")


def get_vars():
    """
    Gets the vars dict associated with the current session,
    or the empty dict if none are set.
    """
    state = get_state()
    return state.get("vars", {})


def set_vars(vars_dict):
    """
    Sets the vars dict associated with the current session.
    """
    state = get_state()
    state["vars"] = vars_dict
    set_state(state)


def show_vars(vars_dict):
    """
    Shows the var, value items in the state.
    """
    if vars_dict:
        for (name, [method, value]) in vars_dict.items():
            if method == "literal":
                print("{Name}\t\"{Value}\"".format(
                    Name=name,
                    Value=value))
            elif method == "read":
                print("{Name}\t<{Value}>".format(
                    Name=name,
                    Value=value))
    else:
        print("No vars")


def command(args):
    """
    Optionally clears all existing vars, then sets one or more vars
    ready to be used in subsequent operation calls. Var values can
    be supplied as literals, or read from files.

    If no arguments are supplied, shows current var values.
    """
    vars_dict = get_vars()

    if not (args.clear or args.literal or args.read):
        show_vars(vars_dict)

    if args.clear:
        vars_dict = {}

    if args.literal:
        for (name, value) in args.literal:
            vars_dict[name] = ["literal", value]

    if args.read:
        for (name, value) in args.read:
            vars_dict[name] = ["read", value]

    set_vars(vars_dict)
