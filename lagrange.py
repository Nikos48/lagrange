"""
A sympy-based Lagrange polynomial constructor.

Given a set of function inputs and outputs, the lagrangePolynomial function will construct an
expression that for every input gives the corresponding output. For intermediate values,
the polynomial interpolates (giving varying results based on the shape of your input).
This is useful when the result needs to be used outside of Python, because the
expression can easily be copied. To convert the expression to a python function object,
use sympy.lambdify.
"""
from sympy import *

import math

from operator import mul
from functools import reduce, lru_cache
from itertools import chain

# sympy symbols
x = symbols('x')

# convenience functions
product = lambda *args: reduce(mul, *(list(args) + [1]))

# test data
labels = [(-3/2), (-3/4), 0, 3/4, 3/2]
points = [math.tan(v) for v in labels]

# this product may be reusable (when creating many functions on the same domain)
# therefore, cache the result


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


def x_intersections(function, *args):
    "Finds all x for which function(x) = 0"
    # solve_poly_system seems more efficient than solve for larger expressions
    return [var for var in chain.from_iterable(solve_poly_system([function], *args)) if (var.is_real)]


def x_scale(function, factor):
    "Scale function on the x-axis"
    return functions.subs(x, x / factor)


if __name__ == '__main__':
    func = lagrangePolynomial(labels, points)

    pyfunc = lambdify(x, func)

    for a, b in zip(labels, points):
        assert(pyfunc(a) - b < 1e-6)

init_printing(use_unicode=False, wrap_line=False, no_global=True)

laga = lagrangePolynomial(
    [0.349, 0.350, 0.351, 0.352, 0.353],
    [0.34196, 0.34290, 0.34384, 0.34478, 0.34488])

print(integrate(laga, (x, 0.349, 0.353)))