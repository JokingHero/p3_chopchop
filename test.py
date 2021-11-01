#!/usr/bin/env python3

import unittest
import re
import os
import testing.end_to_end.TestRunner as tr


def all_tests():
    srch = re.compile("test.*.py$")
    files = os.listdir("testing/unit_tests/")
    files = filter(srch.search, files)

    return files

def run(name):
    name = "testing.unit_tests."+name[:-3]
    unittest.main(module=name,exit=False)

class Test(unittest.TestCase):

    def test_end_to_end(self):
        print("TESTING END_TO_END")
        os.chdir("testing/end_to_end")
        tr.main()


if __name__ == "__main__":
    targets = all_tests()
    print("TESTING UNITS")
    for t in targets:
        run(t)
    unittest.main()
