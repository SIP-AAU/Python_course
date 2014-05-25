"""
A script to compare different root-finding algorithms.

http://scipy-lectures.github.io/advanced/debugging/index.html
This version of the script is buggy and does not execute. It is your task
to find an fix these bugs.

The output of the script sould look like:

    Benching 1D root-finder optimizers from scipy.optimize:
    random_a looks like: array([-0.59600091, -0.72835531, -0.46453783])
              brenth:   599051 total function calls
              brentq:   588283 total function calls
              ridder:   767728 total function calls
              bisect:  2145265 total function calls

"""
from itertools import product

import numpy as np
from scipy import optimize

FUNCTIONS = (np.tan,  # Dilating map
             np.tanh, # Contracting map
             lambda x: x**3 + 1e-4*x, # Almost null gradient at the root
             lambda x: x+np.sin(2*x), # Non monotonous function
             lambda x: 1.1*x+np.sin(4*x), # Fonction with several local maxima
            )

OPTIMIZERS = (optimize.brenth, optimize.brentq, optimize.ridder,
              optimize.bisect)


def apply_optimizer(optimizer, func, a, b):
    """ Return the number of function calls given an root-finding optimizer,
        a function and upper and lower bounds.
    """
    return optimizer(func, a, b, full_output=True)[1].function_calls,


def bench_optimizer(optimizer, param_grid):
    """ Find roots for all the functions, and upper and lower bounds
        given and return the total number of function calls.
    """
    return sum(apply_optimizer(optimizer, func, a, b)
               for func, a, b in param_grid)


def compare_optimizers(optimizers):
    """ Compare all the optimizers given on a grid of a few different
        functions all admitting a signle root in zero and a upper and
        lower bounds.
    """
    random_a = -1.3 + np.random.random(size=100)
    random_b =   .3 + np.random.random(size=100)
    param_grid = product(FUNCTIONS, random_a, random_b)
    print "Benching 1D root-finder optimizers from scipy.optimize:"
    print "random_a looks like: " + random_a[:3]
    for optimizer in OPTIMIZERS:
        print '% 20s: % 8i total function calls' % (
                    optimizer.__name__,
                    bench_optimizer(optimizer, param_grid)
                )


if __name__ == '__main__':
    compare_optimizers(OPTIMIZERS)
