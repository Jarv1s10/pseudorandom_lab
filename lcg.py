from collections import Counter
import pprint


def histogram(self):
    nums = [float(str(num)[:3]) for num in self.generate()]
    counts = Counter(nums)
    res = {}
    for n, c in counts.items():
        key = '[%f; %f]' % (n, n + 0.1)
        res[key] = c / len(nums)
    return res


class CG:
    def __init__(self, iters):
        self.iters = iters
        self.x_value = 123456789  # seed, or X_0 = 123456789
        self.a = 101427  # "a" base value
        self.c = 321  # "c" base value
        self.m = 2 ** 31


class LCG(CG):
    def __init__(self, iters):
        # X_n+1=(aX_n+c) mod m
        CG.__init__(self, iters)

    def __str__(self):
        return str(self.generate())

    def __generate_one(self):
        self.x_value = (self.a * self.x_value + self.c) % self.m
        return self.x_value / self.m

    def generate(self):
        return [self.__generate_one() for _ in range(self.iters)]


class QCG(CG):
    def __init__(self, iters):
        CG.__init__(self, iters)
        self.d = 201433

    def __str__(self):
        return str(self.generate())

    def __generate_one(self):
        self.x_value = (self.d * self.x_value ** 2 + self.a * self.x_value + self.c) % self.m
        return self.x_value / self.m

    def generate(self):
        return [self.__generate_one() for _ in range(self.iters)]


class FibGen:
    def __init__(self, iters):
        self.iters = iters
        self.m = 2 ** 31
        self.j = 3
        self.k = 7
        self.s = [8, 6, 7, 5, 3, 0, 9]

    def __generate_one(self, i):
        out = (self.s[self.j - 1] + self.s[self.k - 1]) % self.m
        for i in range(len(self.s)-1):
            self.s[i] = self.s[i + 1]
        self.s[:-1] = out
        return out

    def generate(self):
        return [self.__generate_one(i) for i in range(self.iters)]

    def __str__(self):
        return str(self.generate())


lcg = LCG(10)
print(lcg)
pprint.pprint(histogram(lcg))

qcg = QCG(10)
print(qcg)
pprint.pprint(histogram(qcg))

#fg = FibGen(10)
#print(fg)
#pprint.pprint(histogram(fg))
