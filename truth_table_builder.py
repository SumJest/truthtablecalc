import typing

import solver


class Builder:
    statement: str
    variables: typing.List[str]

    def __init__(self, statement: str):
        self.statement = statement
        self.variables = self.__get_variables()

    def __get_variables(self):
        variables = []
        for letter in self.statement:
            if ord('z') >= ord(letter) >= ord('a'):
                if letter not in variables:
                    variables.append(letter)
        variables.sort()
        return variables

    def build(self) -> typing.Tuple[typing.List[typing.List[int]], typing.List[int]]:
        """
        Builds a truth table
        :return: A tuple of input data and value
        For example returns:
        ([[0,0],[0,1],[1,0],[1,1]],[0,0,0,1])
        """
        slvr = solver.Solver()
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
            values.append(int(slvr.solve(self.statement, **kwargs)))
        return input_data, values


def main():
    statement = input("Введите выражение: ")

    builder = Builder(statement)
    input_data, values = builder.build()
    print("Таблица истинности: ")
    print(" ".join(builder.variables) + " " + statement)
    for i in range(len(values)):
        print(" ".join(map(str, input_data[i])), end=" ")
        print(" " * (len(statement) // 2) + str(values[i]))


if __name__ == "__main__":
    main()
