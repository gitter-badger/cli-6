"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Session command implementation.
"""
from __future__ import print_function

import sys
import json

from sparkl_cli.common import (
    get_state,
    get_working_dir)

DESCRIPTION = "Shows session state"


def parse_args(_):
    """
    Adds the module-specific subcommand arguments.
    """
    return


def command(args):
    """
    Shows the session directory.
    """
    working_dir = get_working_dir()

    print("session_dir:", working_dir)
    print("session_state:")
    json.dump(
        get_state(), sys.stdout,
        indent=2)
    print()
