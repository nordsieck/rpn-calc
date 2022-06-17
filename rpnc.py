import unittest
from io import StringIO
from sys import stdin, stdout

class Calc:

    def __init__(self):
        self.the_stack = []
        self.temp_stack = [] # the stack during a transaction

    def calculate(self, data):
        value = self.parse(data)
        if value == ERR_INPUT:
            return ERR_INPUT
        return self.execute(value)

    def parse(self, data):
        elements = data.split()
        values = []
        for i in range(len(elements)):
            next = self.parseSingle(elements[i])
            if next == ERR_INPUT:
                return ERR_INPUT
            values.append(next)

        return values

    def parseSingle(self, data):
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

    def execute(self, values):
        last = ""

        # start transaction
        self.temp_stack = self.the_stack.copy()
        for i in range(len(values)):
            last = self.executeSingle(values[i])
            if last == ERR_OPS:
                return ERR_OPS

        # write transaction
        self.the_stack = self.temp_stack
        return last

    def executeSingle(self, value):
        if type(value) is int:
            self.temp_stack.append(value)
            return value

        if len(self.temp_stack) < value.operands:
            return ERR_OPS

        params = []
        for i in range(value.operands):
            params.append(self.temp_stack.pop())

        result = value.fn(*params)
        self.temp_stack.append(result)
        return result

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

ADD = Operator("+", 2, lambda a, b: b + a)
SUB = Operator("-", 2, lambda a, b: b - a)
MUL = Operator("*", 2, lambda a, b: b * a)
DIV = Operator("/", 2, lambda a, b: b / a)

def clInterface(reader, writer):
    calc = Calc()

    writer.write("> ")
    writer.flush()
    for line in reader:
        line = line.strip()
        if line == "q":
            return
        writer.write("{}".format(calc.calculate(line)))
        writer.write("\n> ")

if __name__ == "__main__":
    clInterface(stdin, stdout)

class TestClInterface(unittest.TestCase):
    def testClInterface(self):
        cases = [
            # exit
            ["", "> "],
            ["q\n", "> "],

            # numbers
            ["5\n", "> 5\n> "],
            ["2\n4\n", "> 2\n> 4\n> "],

            # operations
            ["2\n4\n+\n", "> 2\n> 4\n> 6\n> "],
            ["2\n4\n-\n", "> 2\n> 4\n> -2\n> "],
            ["2\n4\n*\n", "> 2\n> 4\n> 8\n> "],
            ["2\n4\n/\n", "> 2\n> 4\n> 0.5\n> "],

            # chain
            ["2\n4\n+\n10\n+\n", "> 2\n> 4\n> 6\n> 10\n> 16\n> "],

            # multiple
            ["1 2 3 - /\n", "> -1.0\n> "],

            # examples
            ["5\n8\n+\n", "> 5\n> 8\n> 13\n> "],
            ["5 8 +\n13 -", "> 13\n> 0\n> "],
            ["-3\n-2\n*\n5\n+\n", "> -3\n> -2\n> 6\n> 5\n> 11\n> "],
            ["5\n9\n1\n-\n/\n", "> 5\n> 9\n> 1\n> 8\n> 0.625\n> "],
            
        ]

        for i in range(len(cases)):
            r = StringIO(cases[i][0])
            w = StringIO()
            clInterface(r, w)
            self.assertEqual(w.getvalue(), cases[i][1])
    
class TestCalc(unittest.TestCase):
    def testParse(self):
        c = Calc()

        # +
        val = c.parse("+")[0]
        self.assertEqual(val.fn(4, 2), 6)

        # -
        val = c.parse("-")[0]
        self.assertEqual(val.fn(4, 2), -2)

        # *
        val = c.parse("*")[0]
        self.assertEqual(val.fn(4, 2), 8)

        # /
        val = c.parse("/")[0]
        self.assertEqual(val.fn(4, 2), 0.5)

        # int
        self.assertEqual(c.parse("5")[0], 5)
        self.assertNotEqual(c.parse("6")[0], 5)
        self.assertEqual(c.parse("w"), ERR_INPUT)

        # multiple
        self.assertEqual(c.parse("1 3 +"), [1, 3, ADD])
        self.assertEqual(c.parse("2, w, -"), ERR_INPUT)

    def testExecute(self):
        c = Calc()

        self.assertEqual(c.the_stack, [])
        self.assertEqual(c.execute([ADD]), ERR_OPS)

        # operators
        cases = [[ADD, 6],
                 [SUB, -2],
                 [MUL, 8],
                 [DIV, 0.5]]

        for i in range(len(cases)):
            c.execute([2])
            c.execute([4])
            self.assertEqual(c.execute([cases[i][0]]), cases[i][1])

        # chain
        c = Calc()
        c.execute([2])
        c.execute([4])
        self.assertEqual(c.execute([ADD]), 6)
        c.execute([10])
        self.assertEqual(c.execute([ADD]), 16)

        # multiple
        c = Calc()
        self.assertEqual(c.execute([2, 4, ADD]), 6)
        c = Calc()
        self.assertEqual(c.execute([2, ADD, 4]), ERR_OPS)
        c = Calc()
        self.assertEqual(c.execute([ADD, 2, 4]), ERR_OPS)
        self.assertEqual(c.execute([ADD]), ERR_OPS)
        self.assertEqual(c.execute([2]), 2)
        self.assertEqual(c.execute([ADD, 4]), ERR_OPS)
        self.assertEqual(c.execute([4, ADD]), 6)
