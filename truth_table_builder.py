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
    """
    Класс для решения логических выражений по типу (1+!1)->(0*1)
    """
    __operators: typing.List[str]  # стэк из операторов
    __operands: typing.List[bool]  # стэк из операндов

    __priorities: typing.Dict[str, int]

    def __init__(self):
        self.__operands = []
        self.__operators = []
        # Приоритеты различных операций, чем меньше значение, тем приоритетней операция
        self.__priorities = {"(": -1, "!": 0, "*": 1, "+": 2, "^": 2, "|": 3, "#": 4, "@": 5, "=": 6}

    def __operate(self):
        """
        Функция производит операцию из 'верха' стека над 'верхними' операндами
        :return:
        """
        op = self.__operators.pop()  # Извлекаем оператор

        b = self.__operands.pop()  # Извлекаем второй операнд
        a = None

        # В случае если оператор не является НЕ, то есть бинарный, то мы извлекаем и первый операнд
        if op != "!":
            a = self.__operands.pop()

        result: bool = False

        # Производим операцию
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

        self.__operands.append(result)  # Кладем результат операции оператно в стэк операндов

    def __can_operate(self, op: str) -> bool:
        """
        Функция проверяет нужно ли произвести операцию
        :param op: потенциальный оператор
        :return:
        """
        # Если стэк операторов пустой, то возвращаем False
        if not len(self.__operators):
            return False
        p1 = self.__priorities[op]  # Приоритет текущего оператора
        p2 = self.__priorities[self.__operators[len(self.__operators) - 1]]  # Приоритет предыдущего оператора

        # В случае если предыдущий оператор приоритетней (значение приоритета меньше), то мы возвращаем True
        # В противном случае возвращаем False
        return (p1 >= 0) and (p2 >= 0) and (p1 >= p2)

    def solve(self, statement: str, is_gaps: bool, **kwargs) -> bool | typing.List[bool]:
        """
        Функция решения логического выражения
        :param statement: Выражение
        :param is_gaps: Требуется ли пошаговый результат
        :param kwargs: Переменные и их значения
        :return: Булевая переменная или их список - результат или пошаговый результат выражения
        """

        # Заменяем все переменные на 1 или 0
        for key in kwargs.keys():
            statement = statement.replace(key, str(int(kwargs[key])))

        statement = statement.replace(" ", "")  # Удалаем пробелы
        statement = "(" + statement + ")"  # Оборачиваем выражение в скобки
        gaps: typing.List[bool] = []  # Список предварительных результатов

        # пробегаемся по всем символам выражения
        for letter in statement:
            # Если это цифра, то заносим её в стэк операндов
            if str.isdigit(letter):
                self.__operands.append(bool(int(letter)))
            else:
                # Если это закрывающаяся скобка, то мы должны выполнить все операции до открывающейся
                if letter == ")":
                    while len(self.__operators) > 0 and self.__operators[len(self.__operators) - 1] != "(":
                        self.__operate()
                        # Заносим предварительный результат если необходимо
                        if is_gaps:
                            gaps.append(self.__operands[len(self.__operands) - 1])
                    self.__operators.pop()  # Удаляем открывающуюся скобку
                else:
                    # Циклично проверяем, нужно ли выполнить операцию и выполняем
                    while self.__can_operate(letter):
                        self.__operate()  # Производим операцию
                        # Заносим предварительный результат если необходимо
                        if is_gaps:
                            gaps.append(self.__operands[len(self.__operands) - 1])
                    self.__operators.append(letter)  # Заносим в стэк оператор, который мы прочитали
            # print(letter)
            # print(self.operators)
            # print(self.operands)
            # print("-----------")

        # В случае если предварительные результаты не заполнялись,
        # берём из стэка последний операнд, он и будет результатом выражения
        result = self.__operands.pop()
        # Очищаем стэки
        self.__operators.clear()
        self.__operands.clear()
        # Возвращаем предварительные результаты (основной результат уже будет там) или основной результат
        return gaps if is_gaps else result


class Breaker:
    """
    Класс для разбиения строки выражения на подвыражения в порядке выполнения
    Этот класс работает по тому же принципу, что и Solver, но он не считает результат
    """
    __operators: typing.List[str]
    __operands: typing.List[str]

    __priorities: typing.Dict[str, int]

    def __init__(self):
        self.__operands = []
        self.__operators = []
        self.__priorities = {"(": -1, "!": 0, "*": 1, "+": 2, "^": 2, "|": 3, "#": 4, "@": 5, "=": 6}

    def __operate(self) -> str:
        """
        Результатом этой функции будет строка вида [операндА]{оператор}{операндB}
        Пример: a+b или !b
        :return: Подвыражение
        """
        op = self.__operators.pop()

        b = self.__operands.pop()
        a = None
        if op != "!":
            a = self.__operands.pop()
        result = f"{a if a is not None else ''}{op}{b}"
        self.__operands.append(f"{a if a is not None else ''}{op}{b}")
        return result

    def __can_operate(self, op: str):
        """
        Функция проверяет нужно ли проводить операцию
        :param op: текущий оператор
        :return: Нужно ли
        """
        if not len(self.__operators):
            return False
        p1 = self.__priorities[op]
        p2 = self.__priorities[self.__operators[len(self.__operators) - 1]]
        return (p1 >= 0) and (p2 >= 0) and (p1 >= p2)

    def break_into(self, statement: str) -> typing.List[str]:
        """
        Функция разбивает выражение на подвыражения
        :param statement: Выражения
        :return: Список подвыражений в порядке их выполненния
        """
        statement = statement.replace(" ", "")
        statement = "(" + statement + ")"
        gaps = []
        for letter in statement:

            if ord('z') >= ord(letter) >= ord('a'):
                # Если это буква, то заносим в стэк операндов
                self.__operands.append(letter)
            else:
                if letter == ")":
                    while len(self.__operators) > 0 and self.__operators[len(self.__operators) - 1] != "(":
                        gaps.append(self.__operate())
                    if self.__operators[len(self.__operators) - 1] == "(":
                        # Если последний оператор это открывающая скобка, то т.к. текующий символ это закрывающаяся
                        # нужно обернуть последний операнд в скобки
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
    """
    Класс для построения таблицы истинности
    """
    statement: str  # Выражение
    variables: typing.List[str]  # Переменные
    gaps: typing.List[str]  # Подвыражения

    def __init__(self, statement: str):
        self.statement = statement
        self.variables = self.__get_variables()
        self.gaps = []

    def __get_variables(self):
        """
        Функция возвращает все переменные в выражении
        :return:
        """
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
        Строит таблицу истинности
        :return: Кортеж из двумерного списка значений переменных и списка результатов или
        двумерного списка из предварительных результатов
        """
        self.gaps.clear()
        if is_gaps:
            # Если требуются внести в таблицу значения подвыражений, то разбиваем выражение
            brkr = Breaker()
            self.gaps = brkr.break_into(self.statement)

        slvr = Solver()

        count = 2 ** (len(self.variables))  # Количество строк в таблице, то есть количество комбинаций всех переменных
        input_data = [[] for i in range(count)]  # Инициализируем двумерный список для значений переменных
        values = []  # Список всех значений выражения

        # Пробегаемся от 0 до count-1
        for i in range(count):
            kwargs = {}  # Инициализируем словарь для значений каждой переменной

            # В этом цикле мы пробегаемся по каждой переменной и задаем ей значение
            # Т.к. у нас есть счетчик i, то для каждой переменной будет соответствовать каждый бит значения счетчика
            # Счетчик j будет отвечает за порядкой номер бита с конца,
            # то есть 0 бит это 1 переменная, 1 бит это 2 переменная и т.д.
            # К примеру у нас есть переменные a и b, то когда счетчик i будет на 2 (10 в двоичной системе),
            # Значение переменной а = 1, b = 0.
            for j in range(len(self.variables)):  # Пробегаемся от 0 до количества переменных - 1
                value = bool(i & (1 << (len(self.variables) - j - 1)))  # С помощью побитовых операций узнаем
                # значение j-го бита числа i

                input_data[i].append(int(value))  # заносим в двумерный список в строке i значение
                kwargs[self.variables[j]] = value  # в словаре задаем значение соответствующей переменной
            if is_gaps:
                # Если требуются предварительные шаги, то заносим в список результатов список,
                # который нам вернула функция solve
                values.append(list(map(int, slvr.solve(self.statement, is_gaps=is_gaps, **kwargs))))
            else:
                # Если предварительные шаги не требуются, то заносим в список результатов значение,
                # которое нам вернула функция solve
                values.append(int(slvr.solve(self.statement, is_gaps=is_gaps, **kwargs)))
        return input_data, values  # Возвращаем кортеж, это и будет таблица



def normalise(statement: str) -> str:
    return statement.replace("*", "×").replace("#", "↓").replace("^", "⊕").replace("@", "→").replace("=", "≡")


def main():
    statement = input("Введите выражение: ")

    builder = Builder(statement)
    input_data, values = builder.build(True)
    print("Таблица истинности: ")
    print(" ".join(builder.variables) + " " + " ".join(builder.gaps))
    for i in range(len(values)):
        print(" ".join(map(str, input_data[i])), end="")
        for j in range(len(builder.gaps)):
            print(f"{' ' * (len(builder.gaps[j]) // 2 + 1)}{int(values[i][j])}{' ' * (len(builder.gaps[j]) // 2 - 1)}",
                  end=' ')
        print("")


if __name__ == "__main__":
    main()
