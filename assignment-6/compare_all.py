import numpy as np
from math import sin, pi, exp
import time
from cy_trapz import cy_trapz_f1, cy_trapz_f2, cy_trapz_f3, cy_trapz_f4

def run_full_comparison():
    # Test cases with analytical solutions
    test_cases = [
        (f1, cy_trapz_f1, 0, 1, 1000, 1/3),              # ∫x² dx from 0 to 1 = 1/3
        (f2, cy_trapz_f2, 0, pi, 1000, 2),               # ∫sin(x) dx from 0 to π = 2
        (f3, cy_trapz_f3, 0, 1, 1000, exp(1) - 1),       # ∫e^x dx from 0 to 1 = e - 1
        (f4, cy_trapz_f4, 1, 2, 1000, np.log(2))         # ∫1/x dx from 1 to 2 = ln(2)
    ]

    print("Test Cases Results:")
    print("-" * 50)
    for py_f, cy_f, a, b, n, analytical in test_cases:
        print(f"\nTest case: {py_f.__name__} from {a} to {b}")
        x = np.linspace(a, b, n+1)
        y = np.array([py_f(xi) for xi in x])
        
        # Python
        start = time.time()
        py_result = py_trapz(py_f, a, b, n)
        py_time = time.time() - start
        
        # Cython
        start = time.time()
        cy_result = cy_f(a, b, n)
        cy_time = time.time() - start
        
        # NumPy
        start = time.time()
        np_result = np.trapz(y, x)
        np_time = time.time() - start
        
        results = {
            'Python': (py_result, py_time),
            'Cython': (cy_result, cy_time),
            'NumPy': (np_result, np_time)
        }
        
        for method, (result, exec_time) in results.items():
            error = abs(result - analytical)
            print(f"\n{method}:")
            print(f"Result: {result:.10f}")
            print(f"Error: {error:.10e}")
            print(f"Time: {exec_time:.6f} seconds")

    # Performance test with 10 million trapezoids
    print("\nPerformance Test (x² from 0 to 10 with 10M trapezoids):")
    print("-" * 50)
    n = 10_000_000
    analytical = 1000/3  # ∫x² dx from 0 to 10 = 1000/3
    
    for method in ['Python', 'Cython', 'NumPy']:
        start = time.time()
        if method == 'Python':
            result = py_trapz(f1, 0, 10, n)
        elif method == 'Cython':
            result = cy_trapz_f1(0, 10, n)
        else:  # NumPy
            x = np.linspace(0, 10, n+1)
            y = x * x
            result = np.trapz(y, x)
        exec_time = time.time() - start
        error = abs(result - analytical)
        
        print(f"\n{method}:")
        print(f"Time: {exec_time:.6f} seconds")
        print(f"Error: {error:.10e}")

if __name__ == "__main__":
    run_full_comparison()
