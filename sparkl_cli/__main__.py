"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Main module implementing CLI for managing running SPARKL nodes.

This must be invoked as a package, to allow the relative import
of the command files to work:

  python -m sparkl_cli <cmd> <arg..>

Client state between invocations is maintained in the filesystem.
"""

from . import common
from . import cmd_accept

COMMANDS = {
    "accept": cmd_accept.command}


def main():
    """
    Main function performs a garbage collection of temp directories
    and then dispatches according to the command.
    """
    common.garbage_collect()

    working_dir = common.get_working_dir()
    args = common.get_args()

    print "Command is " + args.cmd
    print "Package is " + __package__
    print "Name is " + __name__
    print working_dir
    print args.args

    try:
        dispatch = COMMANDS[args.cmd]
        dispatch(args.args)
    except KeyError:
        print "Unrecognized command: " + args.cmd

if __name__ == "__main__":
    main()
