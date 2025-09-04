# Inversions

![GitHub License](https://img.shields.io/github/license/RandomKiddo/Inversions)

___

## About

This code is for inversion steps on astrophysical functions (but can also be used generally).
Currently, the user must provide a single-variable inversion function `f` and its derivative function `df`. 
The module path and filename are then passed as a command line argument and the inversion is done.
This module can also be used normally, by important functions in another python file and passing in values.

The code is original but based off of multiple pseudo-algorithms and mathematical formulae. 

**The hybrid inversion is a more robust way of doing inversion. The code is original but the idea comes from Matt Coleman, Research Scientist at Princeton University, who utilized the concept in the Athena++ astrophysical MHD codebase: https://github.com/PrincetonUniversity/athena.**

The steps are as follows:
1. Check relative error.
    a. If error > 0.01, use secant method for one step.
    b. Else use Newton-Raphson for one step.
2. If step goes outside bracketing values, revert to Brent-Dekker (assuming bracketing values are given and exist).
3. Update bracketing values.
Loop untils error < tolerance or n iterations > n max iterations.

The inversion formulae used are (typically) from Wikipedia. <br>
Newton-Raphson: https://en.wikipedia.org/wiki/Newton%27s_method. <br>
Brent-Dekker: https://en.wikipedia.org/wiki/Brent%27s_method. <br>
Secant: https://en.wikipedia.org/wiki/Secant_method. <br>
Bisection: https://en.wikipedia.org/wiki/Bisection_method.

On general root-finding algorithms:
https://en.wikipedia.org/wiki/Root-finding_algorithm.

`Copyright © 2025 RandomKiddo`

___

## Current Implemented Methods

1. Newton-Raphson: `newton_raphson(f, df, y0, tol, max_iter, verbose)`
2. Brent-Dekker: `brent_dekker(f, a, b, tol, max_iter, verbose)`
3. Secant: `secant(f, y0, y1, tol, max_iter, stopping_condition, verbose)`
4. Bisection: `bisection(f, a, b, tol, max_iter, verbose)`
5. Hybrid (as defined above): `hybrid_inversion(f, df, y0, a, b, tol, max_iter, verbose)`

Common parameters: <br>
`f`: The inversion callable function, taking a float and returning a float. <br>
`tol`: The precision or tolerance for the relative error to use for the inversion, defaults to 1e-5. <br>
`max_iter`: The max number of iterations to use in the inversion, defaults to 100. <br>
`verbose`: If convergence warnings should be returned to the console, defaults to True.

> [!NOTE]
> Convergence warnings means warnings that the function could not converge due to issues with precision, iterations, etc. Warnings will still be outputted when caused by swapped bracketed values, faulty initial values, and more.

Other parameters (depending on function): <br>
`df`: The inversion callable derivative function, taking a float and returning a float. <br>
`y0`: The float initial guess value to use. Pick a sensible one for your task. <br>
`y1`: The float second initial guess value to use, where required. Pick a sensible one for your task. <br>
`a`: The left bracketing value, where required. Pick a sensible one for your task. <br>
`b`: The right bracketing value, where required. Pick a sensible one for your task. <br>
`stopping_condition`: Int value representing which stopping condition to use (1, 2, or 3), defaults to 1.

> [!IMPORTANT]
> On the stopping condition (which is utilized for the *secant* method), we have three different possible conditions: <br>
> 1. Calculate error using $|y_0-y_1| < \varepsilon$. 
> 2. Calculate error using $|y_0/y_1 - 1| < \varepsilon$. 
> 3. Calculate error using $|f(y_1)| < \varepsilon$.
>
> For a given tolerance $\varepsilon$. <br>
> If any other integer is given, the default behavior is then 1. <br>
___

## Command Line Usage

> [!WARNING]
> The command line usage has some behavior that is currently being updated. Also, the command line arguments are being updated to work with the newer inversion methods. This README will be updated once that work is finished.

Using the command line leverages an `ArgumentParser`. The only required argument is the `.py` file with the required functions.  

> [!IMPORTANT]
> Since the module has no way of knowing which inversion you will use, when using the command line, it is required to define a callable function `f` and a callable derivative function `df`. If you know beforehand that you will be using an inversion technique not requiring `df`, it still must be defined, but you can save some time by defining it trivially:
> ```py
> def df(x: float) -> float:
>    return 0.0
> ```

___

## Usage via Module

Using this code like a module means utilizing the source code on a local storage or accessible cloud storage location.

Clone the repository using HTTPS:
```sh
git clone https://github.com/RandomKiddo/Inversions.git
```

or clone the repository using SSH:
```sh
git clone git@github.com:RandomKiddo/Inversions.git
```

You can then move the `inversions.py` file to wherever its needed, or using Python's `sys` module, you can append the location of the file to your path:
```py
import sys
sys.path.insert(0, '/path/to/directory/of/inversions/module/')
```

Then, in a python file or python shell, the module can be imported by:
```py
from inversion import *
```

and then used:
```py
def f(x: float) -> float:
    return (x+3)*(x-1)**2

brent_dekker(f, -4, 4/3)
```

___


[Back to Top](#inversions)

<sub>This page was last edited on 09.04.2025</sub>