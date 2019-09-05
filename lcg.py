from collections import Counter
import pprint
import matplotlib.pyplot as plt


def histogram(self):
    nums = [self.generate() for _ in range(10)]
    print(nums)
    plt.hist(nums, bins=20)
    plt.ylabel('Distribution')
    plt.show()


class CG:
    def __init__(self):
        self.x_value = 123456789
        self.a = 101427
        self.c = 321
        self.m = 2 ** 31


class LCG(CG):
    def __init__(self):
        # X_n+1=(aX_n+c) mod m
        CG.__init__(self)

    def __str__(self):
        return str(self.generate())

    def generate(self):
        self.x_value = (self.a * self.x_value + self.c) % self.m
        return self.x_value / self.m


class QCG(CG):
    def __init__(self):
        CG.__init__(self)
        self.d = 201433

    def __str__(self):
        return str(self.generate())

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
        return str(self.generate())


histogram(LCG())

histogram(QCG())

histogram(FibGen())

