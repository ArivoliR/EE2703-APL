import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

# Constants
PLANCK_CONSTANT = 6.62607015e-34
SPEED_OF_LIGHT = 299792458
BOLTZMANN_CONSTANT = 1.380649e-23

def planck(lam, T, h, c, k):
    """Planck's law function with improved numerical stability"""
    numerator = 2 * h * c**2
    exponent = (h * c) / (lam * k * T)
    
    # Use log-sum-exp trick for numerical stability
    log_numerator = np.log(numerator)
    log_denominator = 5 * np.log(lam) + np.log1p(np.exp(-exponent))
    
    return np.exp(log_numerator - log_denominator)

def load_data(file_path):
    """Load data from file"""
    try:
        data = np.loadtxt(file_path, delimiter=',')
        return data[:, 0], data[:, 1]
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)

def fit_temperature(x, y):
    """Fit temperature keeping h, c, k constant"""
    def planck_T(lam, T):
        return planck(lam, T, PLANCK_CONSTANT, SPEED_OF_LIGHT, BOLTZMANN_CONSTANT)
    
    T_guess, cov_T = curve_fit(planck_T, x, y, p0=5500, bounds=(1, 1e5))
    return T_guess[0], np.sqrt(cov_T[0][0])

def fit_constants(x, y, T):
    """Fit h, c, k keeping T constant"""
    def planck_hck(lam, h, c, k):
        return planck(lam, T, h*PLANCK_CONSTANT, c*SPEED_OF_LIGHT, k*BOLTZMANN_CONSTANT)
    
    initial_guess = [1, 1, 1]  # Initial guess for scaling factors
    params, cov = curve_fit(planck_hck, x, y, p0=initial_guess, bounds=(1e-10, 1e10))
    return params, cov

def fit_all_parameters(x, y):
    """Fit all parameters T, h, c, k"""
    def planck_all(lam, T, h, c, k):
        return planck(lam, T, h, c, k)
    
    initial_guess = [5500, PLANCK_CONSTANT, SPEED_OF_LIGHT, BOLTZMANN_CONSTANT]
    lower_bounds = [1, 1e-35, 1e5, 1e-25]
    upper_bounds = [1e5, 1e-33, 1e9, 1e-22]
    params, cov = curve_fit(planck_all, x, y, p0=initial_guess, bounds=(lower_bounds, upper_bounds))
    return params, cov

def plot_data(x, y, title, xlabel, ylabel):
    """Plot data"""
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_comparison(x, y_original, y_fitted, title, xlabel, ylabel):
    """Plot comparison between original and fitted data"""
    plt.figure(figsize=(10, 6))
    plt.plot(x, y_original, label='Original')
    plt.plot(x, y_fitted, label='Fitted')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Please provide the input file path as a command-line argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    x, y = load_data(file_path)

    plot_data(x, y, "Original Data", "Wavelength", "Spectral Radiance")

    # Fit temperature
    T, T_std = fit_temperature(x, y)
    print(f"Fitted Temperature (keeping h, c, k constant): {T:.2f} K")
    print(f"Temperature Standard Deviation: {T_std:.2f} K")

    y_T_fit = planck(x, T, PLANCK_CONSTANT, SPEED_OF_LIGHT, BOLTZMANN_CONSTANT)
    plot_comparison(x, y, y_T_fit, "Original vs T-fitted Curve", "Wavelength", "Spectral Radiance")

    # Fit h, c, k
    params, cov = fit_constants(x, y, T)
    print("\nFitted parameters (scaling factors for h, c, k):")
    print(params)
    print("\nCovariance matrix:")
    print(cov)

    y_final = planck(x, T, params[0]*PLANCK_CONSTANT, params[1]*SPEED_OF_LIGHT, params[2]*BOLTZMANN_CONSTANT)
    plot_comparison(x, y, y_final, "Original vs Final Fitted Curve (T fixed)", "Wavelength", "Spectral Radiance")

    # Fit all parameters
    all_params, all_cov = fit_all_parameters(x, y)
    print("\nFitted parameters (T, h, c, k) with no constants fixed:")
    print(f"T = {all_params[0]:.2f} K")
    print(f"h = {all_params[1]:.2e} J⋅s")
    print(f"c = {all_params[2]:.2e} m/s")
    print(f"k = {all_params[3]:.2e} J/K")
    print("\nCovariance matrix:")
    print(all_cov)

    y_all_fit = planck(x, *all_params)
    plot_comparison(x, y, y_all_fit, "Original vs All Parameters Fitted Curve", "Wavelength", "Spectral Radiance")

if __name__ == "__main__":
    main()
