import unittest

class TestCalc(unittest.TestCase):
    # multiply() block
    def test_str_multiply(self):
        # test string case
        self.assertEqual('22', '22'*4)
