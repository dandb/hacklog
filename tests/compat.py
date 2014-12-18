# compatibility with python2.6 unittest
import unittest

if hasattr(unittest.TestCase, 'assertIsInstance'):
    class _Compat: pass
else:
    class _Compat:
        def assertIsInstance(self, obj, cls, msg=None):
           if not isinstance(obj, cls):
	       standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
	       self.fail(self._formatMessage(msg, standardMsg))
