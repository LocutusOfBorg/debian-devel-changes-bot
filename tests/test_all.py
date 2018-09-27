#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Debian Changes Bot
#   Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest


def suite():
    suite = unittest.TestSuite()
    for _, _, files in os.walk("."):
        for name in filter(is_test, files):
            tests = unittest.defaultTestLoader.loadTestsFromName(name[:-3])
            suite.addTests(tests)
    return suite


def is_test(filename):
    return filename.startswith("test_") and filename.endswith(".py")


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
