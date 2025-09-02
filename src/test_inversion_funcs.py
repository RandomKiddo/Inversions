from inversion import *

def f(x: float) -> float:
    return (x+3)*(x-1)**2


def df(x: float) -> float:
    2*(x-1)*(x-3) + (x-1)**2


print(brent_dekker(f, -4, 4/3))