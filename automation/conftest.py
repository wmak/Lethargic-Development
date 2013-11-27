import os
import os.path
import py
import sys
import random

def pytest_configure(config):
    sys.path.append(os.path.join(os.getcwd(), "modules"))

def pytest_runtest_makereport(__multicall__, item, call):
    if call.when == "call":
        try:
            assert([] == item.parent.obj.verificationErrors)
        except AssertionError:
            call.excinfo = py.code.ExceptionInfo()
            print "\nERRORS: "
            for a in item.parent.obj.verificationErrors:
                print a

    report = __multicall__.execute()

    item.outcome = report.outcome

    if call.when == "call":
        if hasattr(item.parent.obj, 'config') and item.parent.obj.config.getboolean('SauceLabs', 'ondemand'):
            s = saunter.saucelabs.SauceLabs(item, report)

    return report

def pytest_runtest_teardown(__multicall__, item):
    __multicall__.execute()

    if hasattr(item.parent.obj, 'config') and item.parent.obj.config.getboolean('SauceLabs', 'ondemand'):
        s = saunter.saucelabs.SauceLabs(item)
