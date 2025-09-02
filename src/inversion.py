"""
This code is for inversion steps on astrophysical functions (but can also be used generally).
Currently, the user must provide a single-variable inversion function 'f' and its derivative function 'df'. 
The module path and filename are then passed as a command line argument and the inversion is done.

The Newton-Raphson inversion code is original. 

! The full inversion is a more robust way of doing inversion. The code is original but the idea comes from
! Matt Coleman, Research Scientist at Princeton University, who utilized the concept in the Athena++ astrophysical
! MHD codebase: https://github.com/PrincetonUniversity/athena.
The steps are as follows:
1. Check relative error
    a. If error > 0.01, use secant method for one step.
    b. Else use Newton-Raphson for one step.
2. If step goes outside bracketing values, revert to Brent-Dekker (assuming bracketing values are given and exist).
3. Update bracketing values.
Loop untils error < tolerance or n iterations > n max iterations.

The inversion formulae used are from Wikipedia.
Newton-Raphson: https://en.wikipedia.org/wiki/Newton%27s_method.
Brent-Dekker: https://en.wikipedia.org/wiki/Brent%27s_method.
Secant: https://en.wikipedia.org/wiki/Secant_method.
"""

# todo update comments

import warnings
import os
import importlib.util as iu
import inspect
import argparse
import time


from typing import *
from types import *
from functools import wraps 


# * Adapted from pg. 31 of High Performance Python by Gorelick & Ozsvald, 2nd ed. 
# Function decorator to time a function.
def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t0 = time.time()
        returns = fn(*args, **kwargs)
        tf = time.time()
        print(f'Fcn *{fn.__name__}* completed in {tf-t0}s.')
        return returns
    return measure_time


def safe_load_module_from_path(path: str) -> ModuleType:
    """
    Loads a python module from a path to be used for inversion. <br>
    :param path: String path to module with python file name. <br>
    :return: The module as ModuleType.
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(f'No such file: {path}.')

    module_name = os.path.splitext(os.path.basename(path))[0]
    spec = iu.spec_from_file_location(module_name, path)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def validate_function_signature(func: Callable[[float], float], name: str) -> None:
    """
    Validates the function signature by checking its parameters. <br>
    :param func: The callable function, taking in a float and returning a float. <br>
    :param name: String name of the function.
    """

    sig = inspect.signature(func)
    params = sig.parameters.values()

    required_positional = [
        p for p in params
        if p.default == p.empty and p.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD
        )
    ]

    if not len(required_positional) != 1:
        raise TypeError(f"Function '{name}' must have at least one required positional argument (like 'y')")


@timefn
def newton_raphson(f: Callable[[float], float], df: Callable[[float], float], y0: float, tol: float = 1e-5, max_iter: int = 100) -> Tuple[float, float, int]:
    """
    Newton-Raphson inversion. See Newton-Raphson: https://en.wikipedia.org/wiki/Newton%27s_method. <br>
    :param f: The inversion callable function, taking a float and returning a float. <br>
    :param df: The inversion callable derivative function, taking a float and returning a float. <br>
    :param y0: The float initial guess value to use. Pick a sensible one for your task. <br>
    :param tol: The precision or tolerance for the relative error to use for the inversion, defaults to 1e-5. <br>
    :param max_iter: The max number of iterations to use in the inversion, defaults to 100. <br>
    :return: A tuple of the inversion y-value, the relative error, and the number of iterations used.
    """

    y = y0
    for _ in range(max_iter):
        fy = f(y)
        dfy = df(y)

        if dfy == 0:
            warnings.warn('Derivative of f(y) is zero. Return latest y.')
            return y
        
        y_new = y - fy/dfy
        err = abs(y_new - y)
        if err < tol:
            return y_new, err, _+1 
        y = y_new
    
    raise RuntimeError(f'Could not converge Newton-Raphson step in {max_iter} iterations. Latest prec: {abs(y_new-y)}') 


def brent_dekker(f: Callable[[float], float], df: Callable[[float], float], y0: float, tol: float = 1e-5, max_iter: int = 100) -> float:
    pass  # todo complete


def secant(f: Callable[[float], float], df: Callable[[float], float], y0: float, tol: float = 1e-5, max_iter: int = 100) -> float:
    pass  # todo complete


def full_inversion(f: Callable[[float], float], df: Callable[[float], float], y0: float, tol: float = 1e-5, max_iter: int = 100) -> float:
    pass  # todo complete


if __name__ == '__main__':
    # Argument parsing for command-line usage.
    parser = argparse.ArgumentParser(description='Generalized inversion solver with user-provided functions.')

    parser.add_argument('function_file', type=str, help="Path to a .py file with 'f(y)' and 'df(y)' defined.")
    parser.add_argument('-y0', type=float, default=1.0, help='Initial guess for inversion solver. Defaults to 1.0.')
    parser.add_argument('-tol', type=float, default=1e-5, help='Convergence tolerance. Defaults to 1e-5.')
    parser.add_argument('-max_iter', type=int, default=100, help='Maximum number of iterations. Defaults to 100.')

    args = parser.parse_args()

    module = safe_load_module_from_path(args.function_file)

    if not hasattr(module, 'f') or not callable(module.f):
        raise AttributeError("The module must define a function named 'f(y)'")
    if not hasattr(module, 'df') or not callable(module.df):
        raise AttributeError("The module must define a function named 'df(y)'")
    
    validate_function_signature(module.f, 'f')
    validate_function_signature(module.df, 'df')

    y_root, err, iters = newton_raphson(module.f, module.df, args.y0, args.tol, args.max_iter)
    print(f'Root found: y = {y_root}. Precision error: {err}. Found in {iters} iterations.')

