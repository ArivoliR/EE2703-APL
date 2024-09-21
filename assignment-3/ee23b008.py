"""
Arivoli Ramamoorthy
EE23B008

Assignment-3 Data Estimation
This assignment is based on trying to estimate various physical parameters using raw data (from the datasets) and Planck's formula
Input: Datasets (Spectral radiance vs Wavelength)
Output: Fitted values of h c k T.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

# Constants
PLANCK_CONSTANT = 6.6e-34
SPEED_OF_LIGHT = 300000000
BOLTZMANN_CONSTANT = 1.38e-23

def planck(lam, T, h, c, k):
    """Planck's law function"""
    return (2*h*c**2)/(lam**5 * (np.exp((h*c)/(lam*k*T)) - 1))

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
    
    T_guess, cov_T = curve_fit(planck_T, x, y, p0=5500)
    return T_guess[0], np.sqrt(cov_T[0][0])

def fit_constants(x, y, T):
    """Fit h, c, k keeping T constant"""
    def planck_hck(lam, h, c, k):
        return planck(lam, T, h*PLANCK_CONSTANT, c*SPEED_OF_LIGHT, k*BOLTZMANN_CONSTANT)
    
    initial_guess = [1, 1, 1]  # Initial guess for scaling factors
    params, cov = curve_fit(planck_hck, x, y, p0=initial_guess)
    return params, cov

def fit_all_parameters(x, y):
    """Fit all parameters T, h, c, k"""
    def planck_all(lam, T, h, c, k):
        return planck(lam, T, h, c, k)
    
    initial_guess = [5500, PLANCK_CONSTANT, SPEED_OF_LIGHT, BOLTZMANN_CONSTANT]
    params, cov = curve_fit(planck_all, x, y, p0=initial_guess)
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
    print("\nFitted parameters (T fixed, h, c, k fitted):")
    print(f"T = {T:.2f} K")
    print(f"h = {params[0]*PLANCK_CONSTANT:.2e} J⋅s")
    print(f"c = {params[1]*SPEED_OF_LIGHT:.2e} m/s")
    print(f"k = {params[2]*BOLTZMANN_CONSTANT:.2e} J/K")
    #print("\nCovariance matrix:")
    #print(cov)

    y_final = planck(x, T, params[0]*PLANCK_CONSTANT, params[1]*SPEED_OF_LIGHT, params[2]*BOLTZMANN_CONSTANT)
    plot_comparison(x, y, y_final, "Original vs Final Fitted Curve (T fixed)", "Wavelength", "Spectral Radiance")

    # Fit all parameters
    all_params, all_cov = fit_all_parameters(x, y)
    print("\nFitted parameters (T, h, c, k) with no constants fixed:")
    print(f"T = {all_params[0]:.2f} K")
    print(f"h = {all_params[1]:.2e} J⋅s")
    print(f"c = {all_params[2]:.2e} m/s")
    print(f"k = {all_params[3]:.2e} J/K")
    #print("\nCovariance matrix:")
    #print(all_cov)

    y_all_fit = planck(x, *all_params)
    plot_comparison(x, y, y_all_fit, "Original vs All Parameters Fitted Curve", "Wavelength", "Spectral Radiance")

if __name__ == "__main__":
    main()
