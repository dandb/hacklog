#! /usr/bin/env python

import unittest, sys 
sys.path.append('hacklog')

def load_tests(loader, tests, pattern):
  ''' 
  Discover and load all unit tests in all files named ``*_test.py`` in ``.``
  '''
  suite = unittest.TestSuite()
  for all_test_suite in unittest.defaultTestLoader.discover('.', pattern='*_test.py'):
    for test_suite in all_test_suite:
      suite.addTests(test_suite)
  return suite

def main():
   unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
   unittest.main()
