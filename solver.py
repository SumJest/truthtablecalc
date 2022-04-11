import typing


# "!" - NOT
# "*" - AND
# "+" - OR
# "^" - XOR
# "|" - NAND
# "#" - NOR
# "@" - IMP
# "=" - EQU
class Solver:
    operators: typing.List[str]
    operands: typing.List[bool]

    priorities: typing.Dict[str, int]

    def __init__(self):
        self.operands = []
        self.operators = []
        self.priorities = {"(": -1, "!": 0, "*": 1, "+": 2, "^": 2, "|": 3, "#": 4, "@": 5, "=": 6}

    def __operate(self):
        op = self.operators.pop()

        b = self.operands.pop()
        if op != "!":
            a = self.operands.pop()
        result: bool = False

        if op == "!":
            result = not b
        elif op == "*":
            result = a and b
        elif op == "+":
            result = a or b
        elif op == "^":
            result = a != b
        elif op == "|":
            result = not (a and b)
        elif op == "#":
            result = not (a or b)
        elif op == "@":
            result = not a or b
        elif op == "=":
            result = a == b
        else:
            pass
            # Raise and exception
        self.operands.append(result)

    def __can_operate(self, op: str):
        if not len(self.operators):
            return False
        p1 = self.priorities[op]
        p2 = self.priorities[self.operators[len(self.operators) - 1]]
        return (p1 >= 0) and (p2 >= 0) and (p1 >= p2)

    def solve(self, statement: str, **kwargs) -> bool:

        for key in kwargs.keys():
            statement = statement.replace(key, str(int(kwargs[key])))
        statement = statement.replace(" ", "")
        statement = "(" + statement + ")"
        for letter in statement:
            if str.isdigit(letter):
                self.operands.append(bool(int(letter)))
            else:
                if letter == ")":
                    while len(self.operators) > 0 and self.operators[len(self.operators) - 1] != "(":
                        self.__operate()
                    self.operators.pop()
                else:
                    while self.__can_operate(letter):
                        self.__operate()
                    self.operators.append(letter)
            # print(letter)
            # print(self.operators)
            # print(self.operands)
            # print("-----------")
        return self.operands.pop()
