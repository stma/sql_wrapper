#This file is part of dbretriever.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import sys
import os
import unittest
import doctest
import sql

here = os.path.dirname(__file__)
readme = os.path.normpath(os.path.join(here, '..', '..', 'README'))


def test_suite():
    suite = unittest.TestSuite()
#    additional_tests(suite)
    loader = unittest.TestLoader()
    for fn in os.listdir(here):
        if fn.startswith('test') and fn.endswith('.py'):
            modname = 'dbretriever.tests.' + fn[:-3]
            __import__(modname)
            module = sys.modules[modname]
            suite.addTests(loader.loadTestsFromModule(module))
    return suite


def additional_tests(suite):
    for mod in (sql,):
        suite.addTest(doctest.DocTestSuite(mod))
    if os.path.isfile(readme):
        suite.addTest(
            doctest.DocFileSuite(
                readme,
                module_relative=False,
                tearDown=lambda t: sql.Flavor.set(sql.Flavor())
            )
        )
    return suite


def main():
    suite = test_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    sys.path.insert(
        0,
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )
    main()
