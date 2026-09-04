"""
Lyapunov Exponents & Quantitative Chaos Analysis Laboratory
Calculates the Largest Lyapunov Exponent (LLE) using Benettin's continuous renormalization method.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Callable, Dict, List, Tuple, Optional

try:
    from nonlinear_oscillators import DuffingOscillator
    from forcing import SinusoidalForcing
except ImportError:
    print("Warning: Prior milestone modules not found. Some features may be limited.")

class LyapunovAnalyzer:
    def __init__(self, ode_func: Callable, dimension: int):
        """
        Generic interface for dynamical systems. 
        ode_func must have the signature: f(t, y) returning dy/dt.
        """
        self.ode_func = ode_func
        self.dimension = dimension

    def numerical_jacobian(self, t: float, y: np.ndarray, h: float = 1e-6) -> np.ndarray:
        """Approximates the Jacobian matrix J = df/dy using central finite differences."""
        J = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            y_plus = np.copy(y)
            y_minus = np.copy(y)
            y_plus[i] += h
            y_minus[i] -= h
            
            f_plus = np.array(self.ode_func(t, y_plus))
            f_minus = np.array(self.ode_func(t, y_minus))
            
            J[:, i] = (f_plus - f_minus) / (2 * h)
        return J

    def calculate_largest_lyapunov(self, y0: np.ndarray, t_start: float = 0.0, 
                                   t_max: float = 500.0, tau_r: float = 1.0, 
                                   delta0: float = 1e-8, transient_time: float = 100.0,
                                   method: str = 'RK45', rtol: float = 1e-8, atol: float = 1e-8) -> Dict:
        """
        Calculates the Largest Lyapunov Exponent using Benettin's renormalization method.
        """
        if transient_time > 0:
            # Evolve to discard transient
            sol_trans = solve_ivp(self.ode_func, (t_start, t_start + transient_time), y0, 
                                  method=method, rtol=rtol, atol=atol)
            if not sol_trans.success:
                raise RuntimeError("Transient integration failed.")
            y_ref = sol_trans.y[:, -1]
            t_curr = t_start + transient_time
        else:
            y_ref = np.array(y0, dtype=float)
            t_curr = t_start

        # Initialize perturbation
        perturbation = np.random.randn(self.dimension)
        perturbation = delta0 * (perturbation / np.linalg.norm(perturbation))
        y_pert = y_ref + perturbation

        num_steps = int((t_max - transient_time) / tau_r)
        
        times = []
        local_lyapunovs = []
        cumulative_lyapunovs = []
        S_N = 0.0
        
        for i in range(1, num_steps + 1):
            t_next = t_curr + tau_r
            
            # Evolve Reference
            sol_ref = solve_ivp(self.ode_func, (t_curr, t_next), y_ref, method=method, rtol=rtol, atol=atol)
            # Evolve Perturbed
            sol_pert = solve_ivp(self.ode_func, (t_curr, t_next), y_pert, method=method, rtol=rtol, atol=atol)
            
            if not (sol_ref.success and sol_pert.success):
                return {'converged': False, 'error': 'Integration diverged. Check parameters/solver.'}
                
            y_ref = sol_ref.y[:, -1]
            y_pert = sol_pert.y[:, -1]
            
            # Calculate Separation
            diff = y_pert - y_ref
            d1 = np.linalg.norm(diff)
            
            # Protection against numerical collapse
            if d1 < 1e-15:
                d1 = 1e-15
            elif np.isnan(d1) or np.isinf(d1):
                return {'converged': False, 'error': 'Separation blew up to NaN/Inf.'}

            # Accumulate log growth
            growth_factor = d1 / delta0
            S_N += np.log(growth_factor)
            
            # Renormalize
            diff_norm = diff / d1
            y_pert = y_ref + delta0 * diff_norm
            
            t_curr = t_next
            
            # Record diagnostics
            times.append(t_curr)
            local_lyapunovs.append(np.log(growth_factor) / tau_r)
            cumulative_lyapunovs.append(S_N / (i * tau_r))

        # Convergence diagnostic: Check if the last 10% of cumulative estimates are stable
        final_le = cumulative_lyapunovs[-1]
        tail = cumulative_lyapunovs[int(0.9 * len(cumulative_lyapunovs)):]
        variation = np.max(tail) - np.min(tail)
        converged = variation < 0.05
        
        # Candidate Classification
        if not converged: classification = "numerically_uncertain"
        elif final_le < -1e-3: classification = "stable_candidate"
        elif abs(final_le) <= 1e-3: classification = "periodic_quasiperiodic_candidate"
        else: classification = "chaotic_candidate"

        return {
            'times': np.array(times),
            'local_lyapunov': np.array(local_lyapunovs),
            'cumulative_lyapunov': np.array(cumulative_lyapunovs),
            'lyapunov_exponent': final_le,
            'variation': variation,
            'converged': converged,
            'classification': classification
        }

def run_lyapunov_convergence_experiment(m=1.0, b=0.2, k=-1.0, alpha=1.0, F0=0.3, omega=1.2):
    """Runs a long-time convergence check on a known candidate chaotic Duffing regime."""
    print("\n--- Lyapunov Convergence & Sensitivity Experiment ---")
    forcing = SinusoidalForcing(F0, omega)
    osc = DuffingOscillator(m, b, k, alpha, forcing_function=forcing)
    
    analyzer = LyapunovAnalyzer(osc._ode_system, dimension=2)
    
    res = analyzer.calculate_largest_lyapunov(
        y0=np.array([0.0, 0.0]), t_max=1000.0, tau_r=2.0, delta0=1e-8, transient_time=100.0
    )
    
    print(f"Final Lyapunov Exponent: {res['lyapunov_exponent']:.4f}")
    print(f"Convergence Variation:   {res['variation']:.4e}")
    print(f"Classification:          {res['classification']}")
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("Finite-Time Lyapunov Exponent $\lambda(t)$ Convergence")
    
    axs[0].plot(res['times'], res['local_lyapunov'], 'k-', alpha=0.3, label='Local Growth $\lambda_i$')
    axs[0].set_ylabel("Local LE")
    axs[0].grid(True); axs[0].legend()
    
    axs[1].plot(res['times'], res['cumulative_lyapunov'], 'r-', lw=2, label='Cumulative $\lambda(t)$')
    axs[1].axhline(0, color='b', linestyle='--')
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Cumulative LE")
    axs[1].grid(True); axs[1].legend()
    
    plt.tight_layout()
    plt.show()
    return res

def run_1d_lyapunov_scan(param_name='F0', param_range=(0.25, 0.35), steps=20):
    """Scans a parameter and plots the LLE to identify chaotic transitions."""
    print(f"\n--- 1D Lyapunov Scan over {param_name} ---")
    param_vals = np.linspace(param_range[0], param_range[1], steps)
    le_vals = []
    
    for val in param_vals:
        F0 = val if param_name == 'F0' else 0.3
        forcing = SinusoidalForcing(F0, omega=1.2)
        osc = DuffingOscillator(m=1.0, b=0.2, k=-1.0, alpha=1.0, forcing_function=forcing)
        
        analyzer = LyapunovAnalyzer(osc._ode_system, dimension=2)
        res = analyzer.calculate_largest_lyapunov(y0=np.array([0.1, 0.0]), t_max=500.0, tau_r=1.0, transient_time=50.0)
        
        le = res['lyapunov_exponent'] if res['converged'] else np.nan
        le_vals.append(le)
        print(f"{param_name} = {val:.4f} | LLE = {le:.4f}")
        
    plt.figure(figsize=(10, 5))
    plt.plot(param_vals, le_vals, 'bo-')
    plt.axhline(0, color='k', linestyle='--', label='$\lambda_{max} = 0$ Boundary')
    plt.fill_between(param_vals, 0, le_vals, where=(np.array(le_vals)>0), color='red', alpha=0.3, label='Chaotic Candidate')
    plt.fill_between(param_vals, 0, le_vals, where=(np.array(le_vals)<=0), color='green', alpha=0.3, label='Periodic/Stable')
    plt.title(f"Lyapunov Exponent Scan over {param_name}")
    plt.xlabel(param_name)
    plt.ylabel("Largest Lyapunov Exponent $\lambda_{max}$")
    plt.legend(); plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    res = run_lyapunov_convergence_experiment()
    run_1d_lyapunov_scan()

