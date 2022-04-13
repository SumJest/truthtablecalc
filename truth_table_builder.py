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
    __operators: typing.List[str]
    __operands: typing.List[bool]

    __priorities: typing.Dict[str, int]

    def __init__(self):
        self.__operands = []
        self.__operators = []
        self.__priorities = {"(": -1, "!": 0, "*": 1, "+": 2, "^": 2, "|": 3, "#": 4, "@": 5, "=": 6}

    def __operate(self):
        op = self.__operators.pop()

        b = self.__operands.pop()
        a = None
        if op != "!":
            a = self.__operands.pop()
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
        self.__operands.append(result)

    def __can_operate(self, op: str):
        if not len(self.__operators):
            return False
        p1 = self.__priorities[op]
        p2 = self.__priorities[self.__operators[len(self.__operators) - 1]]
        return (p1 >= 0) and (p2 >= 0) and (p1 >= p2)

    def solve(self, statement: str, is_gaps: bool, **kwargs) -> bool | typing.List[bool]:

        for key in kwargs.keys():
            statement = statement.replace(key, str(int(kwargs[key])))
        statement = statement.replace(" ", "")
        statement = "(" + statement + ")"
        gaps: typing.List[bool] = []
        for letter in statement:
            if str.isdigit(letter):
                self.__operands.append(bool(int(letter)))
            else:
                if letter == ")":
                    while len(self.__operators) > 0 and self.__operators[len(self.__operators) - 1] != "(":
                        self.__operate()
                        if is_gaps:
                            gaps.append(self.__operands[len(self.__operands) - 1])
                    self.__operators.pop()
                else:
                    while self.__can_operate(letter):
                        self.__operate()
                        if is_gaps:
                            gaps.append(self.__operands[len(self.__operands) - 1])
                    self.__operators.append(letter)
            # print(letter)
            # print(self.operators)
            # print(self.operands)
            # print("-----------")
        result = self.__operands.pop()
        self.__operators.clear()
        self.__operands.clear()
        return gaps if is_gaps else result


class Breaker:
    __operators: typing.List[str]
    __operands: typing.List[str]

    __priorities: typing.Dict[str, int]

    def __init__(self):
        self.__operands = []
        self.__operators = []
        self.__priorities = {"(": -1, "!": 0, "*": 1, "+": 2, "^": 2, "|": 3, "#": 4, "@": 5, "=": 6}

    def __operate(self) -> str:
        op = self.__operators.pop()

        b = self.__operands.pop()
        a = None
        if op != "!":
            a = self.__operands.pop()
        result = f"{a if a is not None else ''}{op}{b}"
        self.__operands.append(f"{a if a is not None else ''}{op}{b}")
        return result

    def __can_operate(self, op: str):
        if not len(self.__operators):
            return False
        p1 = self.__priorities[op]
        p2 = self.__priorities[self.__operators[len(self.__operators) - 1]]
        return (p1 >= 0) and (p2 >= 0) and (p1 >= p2)

    def break_into(self, statement: str) -> typing.List[str]:
        statement = statement.replace(" ", "")
        statement = "(" + statement + ")"
        gaps = []
        for letter in statement:
            if ord('z') >= ord(letter) >= ord('a'):
                self.__operands.append(letter)
            else:
                if letter == ")":
                    while len(self.__operators) > 0 and self.__operators[len(self.__operators) - 1] != "(":
                        gaps.append(self.__operate())
                    if self.__operators[len(self.__operators) - 1] == "(":
                        self.__operands[len(self.__operands) - 1] = f'({self.__operands[len(self.__operands) - 1]})'
                    self.__operators.pop()
                else:
                    while self.__can_operate(letter):
                        gaps.append(self.__operate())
                    self.__operators.append(letter)
            # print(letter)
            # print(self.operators)
            # print(self.operands)
            # print("-----------")
        self.__operators.clear()
        self.__operands.clear()
        return gaps


class Builder:
    statement: str
    variables: typing.List[str]
    gaps: typing.List[str]

    def __init__(self, statement: str):
        self.statement = statement
        self.variables = self.__get_variables()
        self.gaps = []

    def __get_variables(self):
        variables = []
        for letter in self.statement:
            if ord('z') >= ord(letter) >= ord('a'):
                if letter not in variables:
                    variables.append(letter)
        variables.sort()
        return variables

    def build(self, is_gaps: bool = False) -> typing.Tuple[
        typing.List[typing.List[int]], typing.List[int] | typing.List[typing.List[int]]]:
        """
        Builds a truth table
        :return: A tuple of input data and value
        For example returns:
        ([[0,0],[0,1],[1,0],[1,1]],[0,0,0,1])
        """
        self.gaps.clear()
        if is_gaps:
            brkr = Breaker()
            self.gaps = brkr.break_into(self.statement)
        slvr = Solver()

        count = 2 ** (len(self.variables))
        input_data = [[] for i in range(count)]
        values = []
        for i in range(count):
            kwargs = {}
            for j in range(len(self.variables)):
                value = bool(i & (1 << (len(self.variables) - j - 1)))
                input_data[i].append(int(value))
                kwargs[self.variables[j]] = value
            # print(" " * (len(self.statement) // 2) + str(int(slvr.solve(self.statement, **kwargs))))
            if is_gaps:
                values.append(list(map(int, slvr.solve(self.statement, is_gaps=is_gaps, **kwargs))))
            else:
                values.append(int(slvr.solve(self.statement, is_gaps=is_gaps, **kwargs)))
        return input_data, values


def normalise(statement: str) -> str:
    return statement.replace("+", "v").replace("*", "∧").replace("#", "↓").replace("^", "⊕").replace("@", "→").replace(
        "=", "↔")


def main():
    statement = input("Введите выражение: ")

    builder = Builder(statement)
    input_data, values = builder.build(True)
    print("Таблица истинности: ")
    print(" ".join(builder.variables) + " " + " ".join(builder.gaps))
    for i in range(len(values)):
        print(" ".join(map(str, input_data[i])), end="")
        for j in range(len(builder.gaps)):
            print(f"{' ' * (len(builder.gaps[j]) // 2 + 1)}{int(values[i][j])}{' ' * (len(builder.gaps[j]) // 2 - 1)}", end=' ')
        print("")


if __name__ == "__main__":
    main()
