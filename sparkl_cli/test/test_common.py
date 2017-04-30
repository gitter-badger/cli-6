"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Test module for common.py
"""
import unittest
import os

from .. import common


class Mock():
    pass


class Tests():
    """
    Basic tests of the common module.
    """
    def setup_method(self):
        common.ARGS = Mock()

    def teardown_method(self):
        pass

    def test_get_working_root(self):
        result = common.get_working_root()
        assert os.path.exists(result)

    def test_get_working_dir(self):
        common.ARGS.session = "1000"
        print common.ARGS
        result = common.get_working_dir()
        assert os.path.exists(result)

    def test_garbage_collect_1(self):
        """
        Garbage collection should remove non-existent pid.
        """
        common.ARGS.session = 123456
        working_dir = common.get_working_dir()
        assert os.path.exists(working_dir)
        common.garbage_collect()
        assert not os.path.exists(working_dir)

    def test_garbage_collect_2(self):
        """
        Garbage collection should not remove live pid.
        """
        common.ARGS.session = os.getppid()
        working_dir = common.get_working_dir()
        assert os.path.exists(working_dir)
        common.garbage_collect()
        assert os.path.exists(working_dir)

    def test_get_state(self):
        common.ARGS.session = 1000
        state = common.get_state()
        assert {} == state

    def test_set_state(self):
        common.ARGS.session = os.getppid()
        state = {
            "connections": {
                "foo": {
                    "url": "some url"}}}
        common.set_state(state)
        result = common.get_state()
        assert state == result
