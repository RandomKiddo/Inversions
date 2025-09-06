# Inversions

![GitHub License](https://img.shields.io/github/license/RandomKiddo/Inversions)

> [!IMPORTANT]
> The latest update has updated the command-line usage so that `df` only needs to be defined in the function file if using Newton-Raphson inversion or hybrid inversion. Otherwise, the inversion will run as expected without needing `df`. 

___

## Table of Contents

- [Inversions](#inversions)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Current Implemented Methods](#current-implemented-methods)
  - [Command Line Usage](#command-line-usage)
  - [Usage via Module](#usage-via-module)
  - [An Important Note on Creating `f` and `df`](#an-important-note-on-creating-f-and-df)

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
    - If error > 0.01, use secant method for one step.
    - Else use Newton-Raphson for one step.
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

Using the command line leverages an `ArgumentParser`. The only required argument is the `.py` file with the required functions.  



Using this code via the command line still requires utilizing the source code on a local storage or accessible clodu storage location.

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

To then use in the command line, you can use any Python installation (Python, Conda, etc.) to run the `inversion.py` file. The below code line may need to be changed depending on the Python instance or the alias for Python (e.g., `python3` instead of `python`).
```sh
python inversion.py "/path/to/inversion/function/file"
```

The "inversion function file" referenced in the above path is a Python file with the inversion functions to be used by the inversion code. Below is a simple example:
```py
def f(x: float) -> float:
    return x**2 + 5

def df(x: float) -> float:
    return 2*x
```

Using the command line python call as above would use default values for all values. Instead, we can use flags to specify values. To see these flags in the command line itself, you can use:
```sh
python inversion.py -h
```
or
```sh
python inversion.py --help
```

Here are a list of the inversion flags you can use (their meanings are the same as the parameters for the inversion functions itself, see [the arguments in this section](#current-implemented-methods) for more info.):<br>

`-y0 Y0`              Initial guess for inversion solver. Defaults to 1.0. <br>
`-tol TOL`          Convergence tolerance. Defaults to 1e-5.<br>
`-max_iter MAX_ITER`  Maximum number of iterations. Defaults to 100.<br>
`-verbose`            If convergence warnings should be returned to the console.<br>
`-y1 Y1`             Initial second guess for inversion solver. Defaults to 0.0.<br>
`-a A`               The left bracketing value. Defaults to 0.0.<br>
`-b B`                The right bracketing value. Defaults to 1.0.<br>
`-stopcon STOPCON`    The int stopping condition number for secant inversion. Defaults to 1.

> [!NOTE]
> For those who have never used command line flags, the capital letters following the flag means that it is asking for a value after a flag. So for a flag like `-verbose`, it requires no values after it, so you can use it as follows (or simply don't include it to exclude its behavior):
> ```sh
> python inversion.py -verbose
> ```
> Whereas, flags like `-y0` expect a value (in this case a float) `Y0` to override the default value of 1.0 (again, in this case). So one uses it as follows (or excludes it if it's not needed or the default value is ok):
> ```sh
> python inversion.py -y0 5.0
> ```

After inputting all the necessary flags (if you know which method you want beforehand, then you can just include the ones you need instead of thinking about all the values), an example command line command will look like:
```sh
python inversion.py test_inversion_funcs.py -a -4 -b 1.3333
```

After running this, the module will prompt which inversion method you like. It will use default arguments if you pick a method that requires values not provided in the shell command. You must enter the integer next to the inversion method you wish to use, and the prompt will continuously repeat if faulty input values are given. Then the inversion will occur, and the root, error, and iterations used will be returned. 

> [!TIP]
> Command line usage is generally best for using static functions (meaning you aren't trying many different `f` and `df`), where the root is the only important step. The values cannot be used in Python after running in the command line. If you wish to do analysis on the results in Python itself (like using the root to then estimate some other value), you should use this code in module form (below).

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

## An Important Note on Creating `f` and `df`

> [!WARNING]
> Creating `f` and `df` for use in inversion is assumed to only take ***one*** positional argument, and return ***one*** value (a float of the value of the function). When using the command line, the method signature is validated for both `f` and `df` so no problems will occur. If, however, you are using this code as a module, the functions are ***not*** checked for validity, which could cause issues when doing inversion. Create functions that only take one positional argument, which should be a float like the following:
> ```py
> def df(x: float) -> float:
>   return 2*x
> ```
> The actual parameter name does not matter. The functions ***must*** be called `f` and `df` for command-line usage. For module usage, the function name does not matter. 

___


[Back to Top](#inversions)

<sub>This page was last edited on 09.05.2025</sub>