import unittest

from RotationProg import hex_to_int

# test class for the rotation program methods
class RotationProgTest(unittest.TestCase):

    def test_hex_to_int(self):
        self.assertEqual(hex_to_int('0D'), 13)
        self.assertEqual(hex_to_int('00'), 0)
        self.assertEqual(hex_to_int('013d'), 317)
        self.assertEqual(hex_to_int('00a6'), 166)

if __name__ == '__main__':
    unittest.main()