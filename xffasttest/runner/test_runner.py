#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import unittest

from xffasttest.runner.test_result import TestResult


class TestRunner(unittest.TextTestRunner):

    def __init__(self, 
                 stream = sys.stderr,
                 descriptions: bool = True,
                 verbosity: int = 1,
                 testresult = None,
                 hook: dict = {}) -> None:
        unittest.TextTestRunner.__init__(self)

        if testresult is None:
            self.testresult = TestResult
        else:
            self.testresult = testresult
        
        self.result = self.testresult(stream = stream,
                                      descriptions = descriptions,
                                      verbosity = verbosity)
        self.hook = hook

    def _setUpModule(self) -> None:
        try:
            self.hook.set_up_global()
        except Exception as e:
            raise e

    def _tearDownModule(self) -> None:
        try:
            self.hook.tear_down_global()
        except Exception as e:
            raise e

    def run(self, test) -> object:
        self._setUpModule()
        test(self.result)
        self._tearDownModule()
        return self.result




