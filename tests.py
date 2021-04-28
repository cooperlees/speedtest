#!/usr/bin/env python3

import unittest

import speedtest_wrapper


# Shitty tests just to ensure file has valid syntax and imports
class TestSpeedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.stc = speedtest_wrapper.SpeedtestCollector()

    def test_stc_valid(self) -> None:
        self.assertTrue(self.stc)
