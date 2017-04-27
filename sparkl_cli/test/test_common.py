"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Test module for common.py
"""
import unittest
import os

from .. import common


class Tests():
    """
    Basic tests of the common module.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_working_root(self):
        result = common.get_working_root()
        assert os.path.exists(result)

    def test_get_working_dir(self):
        common.SESSION_PID = 1000
        result = common.get_working_dir()
        assert os.path.exists(result)

    def test_garbage_collect_1(self):
        """
        Garbage collection should remove non-existent pid.
        """
        common.SESSION_PID = 123456
        working_dir = common.get_working_dir()
        assert os.path.exists(working_dir)
        common.garbage_collect()
        assert not os.path.exists(working_dir)

    def test_garbage_collect_2(self):
        """
        Garbage collection should not remove live pid.
        """
        common.SESSION_PID = os.getppid()
        working_dir = common.get_working_dir()
        assert os.path.exists(working_dir)
        common.garbage_collect()
        assert os.path.exists(working_dir)

    def test_get_state(self):
        common.SESSION_PID = 1000
        state = common.get_state()
        assert {} == state

    def test_set_state(self):
        common.SESSION_PID = os.getppid()
        state = {
            "connections": {
                "foo": {
                    "url": "some url"}}}
        common.set_state(state)
        result = common.get_state()
        assert state == result
