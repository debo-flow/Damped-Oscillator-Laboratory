"""
Milestone 3: Analytical vs Numerical Validation Laboratory
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from damped_oscillator import DampedOscillator
from analytical_solution import AnalyticalSolver

def calculate_errors(num: np.ndarray, ana: np.ndarray) -> dict:
    abs_err = np.abs(num - ana)
    return {
        'abs': abs_err,
        'max': np.max(abs_err),
        'mean': np.mean(abs_err),
        'rms': np.sqrt(np.mean(abs_err**2))
    }

def validate_regime(name: str, m: float, b: float, k: float, x0: float, v0: float):
    print(f"\n--- Running Validation: {name} ---")
    
    # Initialize Solvers
    num_solver = DampedOscillator(m=m, b=b, k=k, x0=x0, v0=v0, duration=10, num_samples=1000)
    ana_solver = AnalyticalSolver(m=m, b=b, k=k, x0=x0, v0=v0)
    
    # 1. Tolerance Study & Convergence
    tolerances = [1e-3, 1e-5, 1e-7, 1e-9]
    print(f"{'Tolerance':<12} | {'Max x Error':<15} | {'RMS x Error'}")
    print("-" * 45)
    
    best_num_res = None
    for tol in tolerances:
        num_res = num_solver.simulate(rtol=tol, atol=tol*1e-3)
        ana_res = ana_solver.solve(num_res['time'])
        
        err_x = calculate_errors(num_res['displacement'], ana_res['displacement'])
        print(f"{tol:<12.0e} | {err_x['max']:<15.3e} | {err_x['rms']:.3e}")
        
        if tol == 1e-9:
            best_num_res = num_res
            
    # 2. Extract best results for plotting/export
    ana_res = ana_solver.solve(best_num_res['time'])
    err_x = calculate_errors(best_num_res['displacement'], ana_res['displacement'])
    err_v = calculate_errors(best_num_res['velocity'], ana_res['velocity'])
    
    # 3. Automated Check
    is_valid = (
        np.all(np.isfinite(best_num_res['displacement'])) and 
        err_x['max'] < 1e-5 and 
        err_v['max'] < 1e-5
    )
    print(f"Validation Status: {'PASS' if is_valid else 'FAIL'}")
    
    export_results(name, best_num_res, ana_res, err_x['abs'], err_v['abs'])
    plot_validation(name, best_num_res, ana_res, err_x['abs'], err_v['abs'])

def export_results(name, num_res, ana_res, err_x, err_v):
    os.makedirs('../results/validation', exist_ok=True)
    filename = f'../results/validation/{name.lower().replace(" ", "_")}_results.csv'
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Ana_Disp', 'Num_Disp', 'Err_Disp', 'Ana_Vel', 'Num_Vel', 'Err_Vel'])
        for i in range(len(num_res['time'])):
            writer.writerow([
                num_res['time'][i], ana_res['displacement'][i], num_res['displacement'][i], err_x[i],
                ana_res['velocity'][i], num_res['velocity'][i], err_v[i]
            ])

def plot_validation(name, num_res, ana_res, err_x, err_v):
    t = num_res['time']
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Validation Laboratory: {name}")

    # Plot 1: Displacement
    axs[0, 0].plot(t, ana_res['displacement'], 'k-', label='Analytical', lw=2)
    axs[0, 0].plot(t, num_res['displacement'], 'r--', label='Numerical')
    axs[0, 0].set_title("Displacement vs Time")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot 2: Velocity
    axs[0, 1].plot(t, ana_res['velocity'], 'k-', label='Analytical', lw=2)
    axs[0, 1].plot(t, num_res['velocity'], 'b--', label='Numerical')
    axs[0, 1].set_title("Velocity vs Time")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot 3: Displacement Error
    axs[1, 0].plot(t, err_x, 'r-')
    axs[1, 0].set_title("Absolute Displacement Error")
    axs[1, 0].set_yscale('log')
    axs[1, 0].grid(True)

    # Plot 4: Velocity Error
    axs[1, 1].plot(t, err_v, 'b-')
    axs[1, 1].set_title("Absolute Velocity Error")
    axs[1, 1].set_yscale('log')
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    validate_regime("Underdamped", m=1.0, b=0.5, k=10.0, x0=1.0, v0=0.0)
    validate_regime("Critically Damped", m=1.0, b=2*np.sqrt(10.0), k=10.0, x0=1.0, v0=0.0)
    validate_regime("Overdamped", m=1.0, b=10.0, k=10.0, x0=1.0, v0=0.0)

