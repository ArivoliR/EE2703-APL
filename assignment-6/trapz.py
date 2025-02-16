# Pure Python implementation
import numpy as np
from math import sin, pi, exp
import time
from typing import Callable

def py_trapz(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """
    Pure Python implementation of the trapezoidal rule.
    
    Args:
        f: Function to integrate
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of trapezoids
        
    Returns:
        Approximate integral value
    """
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return h * s

# Test functions
def f1(x): return x**2  # x^2
def f2(x): return sin(x)  # sin(x)
def f3(x): return exp(x)  # e^x
def f4(x): return 1/x     # 1/x

# Function to compare implementations
def compare_implementations(f: Callable[[float], float], a: float, b: float, n: int, analytical_result: float):
    """
    Compare the three implementations (Python, NumPy) for a given function and parameters.
    
    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of trapezoids
        analytical_result: Known analytical result for comparison
    """
    # Generate x values for NumPy
    x = np.linspace(a, b, n+1)
    y = np.array([f(xi) for xi in x])
    
    # Time Python implementation
    start = time.time()
    py_result = py_trapz(f, a, b, n)
    py_time = time.time() - start
    
    # Time NumPy implementation
    start = time.time()
    np_result = np.trapz(y, x)
    np_time = time.time() - start
    
    # Calculate errors
    py_error = abs(py_result - analytical_result)
    np_error = abs(np_result - analytical_result)
    
    return {
        'Python': {'result': py_result, 'time': py_time, 'error': py_error},
        'NumPy': {'result': np_result, 'time': np_time, 'error': np_error}
    }

# Test cases with analytical solutions
test_cases = [
    (f1, 0, 1, 1000, 1/3),              # ∫x² dx from 0 to 1 = 1/3
    (f2, 0, pi, 1000, 2),               # ∫sin(x) dx from 0 to π = 2
    (f3, 0, 1, 1000, exp(1) - 1),       # ∫e^x dx from 0 to 1 = e - 1
    (f4, 1, 2, 1000, np.log(2))         # ∫1/x dx from 1 to 2 = ln(2)
]

# Run test cases
print("Test Cases Results:")
print("-" * 50)
for f, a, b, n, analytical in test_cases:
    print(f"\nTest case: {f.__name__} from {a} to {b}")
    results = compare_implementations(f, a, b, n, analytical)
    
    for method, data in results.items():
        print(f"\n{method}:")
        print(f"Result: {data['result']:.10f}")
        print(f"Error: {data['error']:.10e}")
        print(f"Time: {data['time']:.6f} seconds")

# Performance test with 10 million trapezoids
print("\nPerformance Test (x² from 0 to 10 with 10M trapezoids):")
print("-" * 50)
results = compare_implementations(f1, 0, 10, 10_000_000, 1000/3)

for method, data in results.items():
    print(f"\n{method}:")
    print(f"Time: {data['time']:.6f} seconds")
    print(f"Error: {data['error']:.10e}")
