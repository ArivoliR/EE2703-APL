# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as np
from libc.math cimport sin, exp, M_PI as pi

ctypedef double (*func_type)(double) nogil

cdef double f1(double x) nogil: return x * x
cdef double f2(double x) nogil: return sin(x)
cdef double f3(double x) nogil: return exp(x)
cdef double f4(double x) nogil: return 1.0 / x

cdef double cy_trapz_impl(func_type f, double a, double b, int n) nogil:
    """
    Cython implementation of the trapezoidal rule.
    """
    cdef:
        double h = (b - a) / n
        double s = 0.5 * (f(a) + f(b))
        int i
        double x
    
    for i in range(1, n):
        x = a + i * h
        s += f(x)
    
    return h * s

# Python-callable wrapper functions
def cy_trapz_f1(double a, double b, int n):
    return cy_trapz_impl(f1, a, b, n)

def cy_trapz_f2(double a, double b, int n):
    return cy_trapz_impl(f2, a, b, n)

def cy_trapz_f3(double a, double b, int n):
    return cy_trapz_impl(f3, a, b, n)

def cy_trapz_f4(double a, double b, int n):
    return cy_trapz_impl(f4, a, b, n)
