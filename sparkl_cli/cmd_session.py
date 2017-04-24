"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Session command implementation.
"""

import sys
import json

from sparkl_cli.common import (
    get_state,
    get_working_dir)


def command(args):
    """
    Shows the session directory.
    """
    argc = len(args)
    if argc != 0:
        print "Usage: session"
        sys.exit(1)

    working_dir = get_working_dir()

    print "session_dir: {SessionDir}".format(
        SessionDir=working_dir)
    print "session_state:"
    json.dump(
        get_state(), sys.stdout,
        indent=2)
    print
