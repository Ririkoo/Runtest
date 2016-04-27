#!/usr/bin/env python
#-*- coding: utf-8 -*-

import runtest

ts = runtest.Tester("it", 1, 10)
teams = {
"Example": "Exmaple",
#Enter team list
}
ts.conftests(teams)
ts.testall()
