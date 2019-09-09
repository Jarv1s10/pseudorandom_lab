import matplotlib.pyplot as plt
import math


def histogram(self):
    plt.hist([self.generate() for _ in range(1000)], bins=10)
    plt.ylabel('Distribution')
    plt.title(self)
    plt.show()


def my_hist(obj, type):
    if type < 6:
        res = [0] * 10
    elif 6 <= type < 9:
        res = [0] * 7
    else:
        res = [0] * 100
    for _ in range(1000):
        num = obj.generate()
        if type < 6:
            # res = [0] * 10
            for i in range(10):
                if i / 10 <= num <= i / 10 + 0.1:
                    res[i] += 1
        elif 6 <= type < 9:
            for i in range(-3, 4):
                if i <= num <= i + 1:
                    res[i + 3] += 1
                    break
        elif 9 <= type <= 10:
            for i in range(101):
                if i <= num <= num + 1:
                    res[i] += 1
    return [round(num / 1000, 2) for num in res]


class LCG:
    def __init__(self):
        self.x_value = 1234
        self.a = 19577
        self.c = 32159
        self.m = 65537

    def __str__(self):
        return "1. Linear congruential generator"

    def generate(self):
        self.x_value = (self.a * self.x_value + self.c) % self.m
        return self.x_value / self.m


class QCG:
    def __init__(self):
        self.x_value = 123456789
        self.a = 101427
        self.c = 321
        self.m = 2 ** 31
        self.d = 201433

    def __str__(self):
        return '2. Quadratic congruential generator'

    def generate(self):
        self.x_value = (self.d * self.x_value ** 2 + self.a * self.x_value + self.c) % self.m
        return self.x_value / self.m


class FibGen:
    def __init__(self):
        self.n = 50
        self.val = 1
        self.m = 2 ** 32

    def __fib(self, num):
        n1, n2 = 1, 1
        for _ in range(num - 2):
            n1, n2 = n2, n1 + n2
        return n2

    def generate(self):
        self.val = (self.__fib(self.n) + self.__fib(self.n - 1)) % self.m
        self.n += 1
        return self.val / self.m

    def __str__(self):
        return '3. Fibonacci numbers generator'


class ICG:
    def __init__(self):
        self.m = 2 ** 8
        self.val = 1
        self.a = 101425
        self.c = 322

    def __imod(self):
        self.val = self.val % self.m
        for x in range(1, self.m):
            if (self.val * x) % self.m == 1:
                return x
        return 1

    def generate(self):
        self.val = (self.a * self.__imod() + self.c) % self.m
        return self.val / self.m

    def __str__(self):
        return '4. Inversive congruential generator'


class UnionGen:
    def __init__(self):
        self.x = LCG()
        self.y = ICG()
        self.val = 0

    def generate(self):
        self.val = (self.x.generate() * self.x.m - self.y.generate() * self.y.m) % self.x.m
        return self.val / self.x.m

    def __str__(self):
        return '5. Union method generator'


class Sigma:
    def __init__(self):
        self.val = 0
        self.ug = UnionGen()

    def generate(self):
        self.val = sum([self.ug.generate() for _ in range(12)]) - 6
        return self.val

    def __str__(self):
        return '6. Rule 3-sigma generator'


class Polar:
    def __init__(self):
        self.v1 = self.v2 = self.u1 = self.u2 = self.s = self.x1 = self.x2 = 0
        self.lcg = LCG()
        self.inv = ICG()

    def __transform(self):
        self.u1 = self.lcg.generate()
        self.u2 = self.inv.generate()
        self.v1 = 2 * self.u1 - 1
        self.v2 = 2 * self.u2 - 1
        self.s = self.v1 ** 2 + self.v2 ** 2
        return self.s

    def generate(self):
        self.s = self.__transform()
        while self.s >= 1:
            self.s = self.__transform()
        self.x1 = self.v1 * math.sqrt(-2 * math.log(self.s) / self.s)
        self.x2 = self.v2 * math.sqrt(-2 * math.log(self.s) / self.s)
        return self.x1 ** 2 + self.x2 * 2

    def __str__(self):
        return '7. Polar coordinates method generator'


class CorrelationGen:
    def __init__(self):
        self.x = self.u = self.v = 0
        self.fib = FibGen()
        self.icg = ICG()

    def __find_x(self):
        while self.u == 0:
            self.u = self.fib.generate()
        self.v = self.icg.generate()
        self.x = math.sqrt(8 / math.e) * (self.v - 0.5) / self.u
        return self.x

    def generate(self):
        self.x = self.__find_x()
        if self.x ** 2 <= 5 - 4 * math.e ** 0.25 * self.u:
            return self.x
        while self.x ** 2 >= (4 * math.e ** (-1.35)) / self.u + 1.4:
            self.x = self.__find_x()
        while self.x ** 2 > -4 * math.log(self.u):
            self.x = self.__find_x()
        return self.x

    def __str__(self):
        return '8. Correlations method generator'


class LogGen:
    def __init__(self):
        self.icg = ICG()
        self.x = 0

    def generate(self):
        self.x = -math.log(self.icg.generate())
        return self.x

    def __str__(self):
        return '9. Logarithm method generator'


class ArensGen:
    def __init__(self):
        self.icg = ICG()
        self.u = self.x = self.v = self.y = 0
        self.a = 10

    def __find_x_y(self):
        self.u = self.icg.generate()
        self.v = self.icg.generate()
        self.y = math.tan(math.pi * self.u)
        self.x = math.sqrt(2 * self.a - 1) * self.y + self.a - 1

    def __check_x(self):
        self.__find_x_y()
        while self.x <= 0:
            self.__find_x_y()

    def generate(self):
        self.__check_x()
        while self.v > (1 + self.y ** 2) * math.exp(
                (self.a - 1) * math.log(self.x / (self.a - 1)) - math.sqrt(2 * self.a - 1) * self.y):
            self.__check_x()
        return self.x

    def __str__(self):
        return '10. Arens method generator'


def menu(number, hist=False):
    generators = {
        1: LCG(), 2: QCG(), 3: FibGen(), 4: ICG(), 5: UnionGen(),
        6: Sigma(), 7: Polar(), 8: CorrelationGen(), 9: LogGen(), 10: ArensGen()
    }
    if hist:
        #histogram(generators[number])
        print(my_hist(generators[number], number))
    return generators[number].generate() if number < 11 else 'wrong number'


def main():
    for i in range(1, 11):
        print(menu(i, hist=True))


if __name__ == '__main__':
    main()
