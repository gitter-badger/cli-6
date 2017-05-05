"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Test module connects to https://demo-instance.sparkl.com:9000
and tests a series of commands.
"""
from .. import main


class Tests():
    """
    Basic tests of the main module.
    """
    def test_version(self):
        assert main.get_version().startswith("sparkl_cli v")
