import matplotlib.pyplot as plt


def histogram(self):
    nums = [self.generate() for _ in range(10)]
    print(nums)
    plt.hist(nums, bins=10)
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
        return str(self.generate())


class UnionGen:
    def __init__(self):
        self.x = FibGen()
        self.y = ICG()
        self.val = 0

    def generate(self):
        self.val = (self.x.generate() * self.x.m - self.y.generate() * self.y.m) % self.x.m
        return self.val / self.x.m


histogram(LCG())

histogram(QCG())

histogram(FibGen())

histogram(ICG())

histogram(UnionGen())