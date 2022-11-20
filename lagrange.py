from sympy import *

from operator import mul
from functools import reduce, lru_cache

# sympy symbols
x = symbols('x')

# convenience functions
product = lambda *args: reduce(mul, *(list(args) + [1]))


@lru_cache(16)
def l(labels, j):
    def gen(labels, j):
        k = len(labels)
        current = labels[j]
        for m in labels:
            if m == current:
                continue
            yield (x - m) / (current - m)
    return expand(product(gen(labels, j)))


def lagrangePolynomial(xs, ys):
    # based on https://en.wikipedia.org/wiki/Lagrange_polynomial#Example_1
    k = len(xs)
    total = 0

    # use tuple, needs to be hashable to cache
    xs = tuple(xs)

    for j, current in enumerate(ys):
        t = current * l(xs, j)
        total += t

    return total


ourPolynomial = lagrangePolynomial(
    [0.349, 0.350, 0.351, 0.352, 0.353],
    [0.34196, 0.34290, 0.34384, 0.34478, 0.34488])

print(integrate(ourPolynomial, (x, 0.349, 0.353)))

#output: 0.00137509647174738
