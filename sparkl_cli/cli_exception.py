"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Exception class allowing formatted errors.
"""


class CliException(Exception):
    """
    Exception raised to stop execution of a command with
    user message.
    """

    def __init__(self, message):
        """
        Sets the user message.
        """
        super(CliException, self).__init__()
        self.message = message

    def __str__(self):
        return "exception: " + self.message
