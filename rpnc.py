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

    def execute(self, value):
        if type(value) is int:
            self.the_stack.append(value)
            return value

        if len(self.the_stack) < value.operands:
            return ERR_OPS

        params = []
        for i in range(value.operands):
            params.append(self.the_stack.pop())

        result = value.fn(*params)
        self.the_stack.append(result)
        return result

    def process(self, data):
        value = self.parse(data)
        if value == ERR_INPUT:
            return ERR_INPUT
        return self.execute(value)

class Error:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

ERR_INPUT = Error("Error: Invalid input")
ERR_OPS   = Error("Error: Insufficient operands")

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

    def testExecute(self):
        c = Calc()

        self.assertEqual(c.the_stack, [])
        self.assertEqual(c.execute(ADD), ERR_OPS)

        # operators
        cases = [[ADD, 6],
                 [SUB, 2],
                 [MUL, 8],
                 [DIV, 2]]

        for i in range(len(cases)):
            c.execute(2)
            c.execute(4)
            self.assertEqual(c.execute(cases[i][0]), cases[i][1])

        # chain
        c = Calc()
        c.execute(2)
        c.execute(4)
        self.assertEqual(c.execute(ADD), 6)
        c.execute(10)
        self.assertEqual(c.execute(ADD), 16)
