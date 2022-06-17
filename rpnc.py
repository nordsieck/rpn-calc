import unittest

class Calc:

    def __init__(self):
        self.the_stack = []

    def parse(self, data):

        try:
            data = int(data)
        except ValueError:
            return ERR_INPUT

        return data

class Error:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

ERR_INPUT = Error("Error: Invalid input")

class TestCalc(unittest.TestCase):
    def testParse(self):
        c = Calc()

        # int
        self.assertEqual(c.parse("5"), 5)
        self.assertNotEqual(c.parse("6"), 5)
        self.assertEqual(c.parse("w"), ERR_INPUT)
