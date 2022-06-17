import unittest

class Calc:

    def __init__(self):
        self.the_stack = []

    def parse(self, data):

        # I currently have python 3.8 installed, would use "match" here with 3.10
        if data == "+":
            return ADD
        if data == "-":
            return SUB
        if data == "*":
            return MUL
        if data == "/":
            return DIV

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

class Operator:
    def __init__(self, text, operands, fn):
        self.text = text
        self.operands = operands
        self.fn = fn

ADD = Operator("+", 2, lambda a, b: a + b)
SUB = Operator("-", 2, lambda a, b: a - b)
MUL = Operator("*", 2, lambda a, b: a * b)
DIV = Operator("/", 2, lambda a, b: a / b)

class TestCalc(unittest.TestCase):
    def testParse(self):
        c = Calc()

        # +
        val = c.parse("+")
        self.assertEqual(val.fn(4, 2), 6)

        # -
        val = c.parse("-")
        self.assertEqual(val.fn(4, 2), 2)

        # *
        val = c.parse("*")
        self.assertEqual(val.fn(4, 2), 8)

        # /
        val = c.parse("/")
        self.assertEqual(val.fn(4, 2), 2)

        # int
        self.assertEqual(c.parse("5"), 5)
        self.assertNotEqual(c.parse("6"), 5)
        self.assertEqual(c.parse("w"), ERR_INPUT)
