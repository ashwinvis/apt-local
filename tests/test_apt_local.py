#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `apt_local` package."""


import unittest
from contextlib import suppress, redirect_stdout
import os
from apt_local import init_parser


class TestAptLocal(unittest.TestCase):
    """Tests for `apt_local` package."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures, if any."""
        cls.parser = init_parser()
        cls.devnull = open(os.devnull, "w")

    @classmethod
    def tearDownClass(cls):
        """Tear down test fixtures, if any."""
        cls.devnull.close()

    def test_help(self):
        """Test something."""
        print("apt-local", "-h")
        with suppress(SystemExit), redirect_stdout(self.devnull):
            args = self.parser.parse_args(["-h"])
        for cmd in (
            "install",
            "uninstall",
            "list",
            "search",
            "set-path",
            "show-path",
        ):
            print("apt-local", cmd, "-h")
            with suppress(SystemExit), redirect_stdout(self.devnull):
                args = self.parser.parse_args([cmd, "-h"])
