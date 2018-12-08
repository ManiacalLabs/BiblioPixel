import os, unittest
from unittest import mock

from bibliopixel.commands import demo
from bibliopixel.main import args, project_flags


class TestDemo(unittest.TestCase):
    def test_demo_projects(self):
        with mock.patch(
                'bibliopixel.animation.animation.Animation.FAIL_ON_EXCEPTION',
                True):
            ARGS = args.set_args('test', [], demo)
            for k, v in demo.demo_table.DEMO_TABLE.items():
                demo.make_runnable_animation(v, ARGS)
