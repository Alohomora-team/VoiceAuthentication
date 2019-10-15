import unittest
import tests.tools_tests

suite = unittest.TestLoader().loadTestsFromModule(tests.tools_tests)
unittest.TextTestRunner(verbosity=2).run(suite)