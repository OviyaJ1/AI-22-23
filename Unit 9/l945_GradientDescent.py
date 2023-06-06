# Oviya Jeyaprakash, 5/14/2023 
# Gradient Descent
# l945

from operator import truth
import numpy as np
import sys
import ast

#f(x, y) = 4x^2 - 3xy + 2y^2 + 24x - 20y
def funcA(x, y):
    return (4*pow(x, 2)) - (3*x*y) + (2*pow(y, 2)) + (24*x) - (20*y)

def funcA_PX(x, y):
    return (8*x) - (3*y) + 24

def funcA_PY(x, y):
    return (4*(y-5)) - (3*x)

#f(x, y) = (1-y)^2 + (x-y^2)^2
def funcB(x, y):
    return pow(1-y, 2) + pow(x-pow(y, 2), 2)

def funcB_PX(x, y):
    return 2*(x-pow(y, 2))

def funcB_PY(x, y):
    return 2*((-2*x*y) + (2*pow(y, 3)) + y - 1)

def result_func(letter, location):
    l = 0.01
    fx = None
    fy = None

    if letter == "A":
        fx = funcA_PX
        fy = funcA_PY
    elif letter == "B":
        fx = funcB_PX
        fy = funcB_PY

    vec = np.array((fx(location[0], location[1]), fy(location[0], location[1])))
    while np.sqrt(vec.dot(vec)) > 0.0000001:
        vec = np.array((fx(location[0], location[1]), fy(location[0], location[1])))
        location = (location[0] - (l*vec[0]), location[1] - (l*vec[1]))
        print(location, vec)
    
result_func(sys.argv[1], (0, 0))