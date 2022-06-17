# rpn-calc

RPN-Calc is a simple commandline program that implements a "reverse polish notation" or postfix calculator; this allows the user to unambiguously specify precedence without using parenthesis. This calculator supports integers, and the following operators: +, -, *, /

Some examples:

    > 1 1 +
    2

    > 5 3 -
    2

#### Reasoning

I tried to isolate the various parts of the code to make it easier to extend.

The core part of the calculator is an object because it is stateful and needs to interact with the interface over time. I tried to make as much of the object (really just the parser) purely function for robustness.

I tried to make the operators as much like data as possible so it should be easy to visually examine them for correctness as well as add new ones.

The user interface is a function because I don't like using objects when they don't seem to be necessary. I tried to make it relatively straightforward to extend.

I prefer to use dependency injection for testing.

I think the temporary stack in the calc object is awkward. It feels like it should be a local variable instead of a field, but it'd make things a little messy since the execute function is split into two parts.

#### How to Run

To run:

    python3 rpnc.py

To test:

    python3 -m unittest rpnc.py