"""
Milestone 10: Nonlinear Oscillators & Duffing Dynamics Laboratory
Simulates the Duffing oscillator, analyzing hardening/softening behaviors, 
amplitude-dependent frequencies, and nonlinear frequency responses.
"""

import os
import csv
import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Dict, Optional, Tuple

try:
    from forcing import ForcingFunction, ZeroForcing, SinusoidalForcing
    from spectral_analysis import SpectralAnalyzer
    from damped_oscillator import DampedOscillator
except ImportError:
    print("Warning: Prior milestone modules not found. Some features may be limited.")

class DuffingOscillator:
    def __init__(self, m: float = 1.0, b: float = 0.5, k: float = 10.0, alpha: float = 1.0,
                 x0: float = 1.0, v0: float = 0.0, duration: float = 30.0, num_samples: int = 3000,
                 forcing_function = None):
        if m <= 0: raise ValueError("Mass (m) must be > 0.")
        if k <= 0: raise ValueError("Linear spring constant (k) must be > 0.")
        if b < 0: raise ValueError("Damping coefficient (b) must be >= 0.")
        if duration <= 0: raise ValueError("Duration must be > 0.")
        
        if alpha < 0:
            warnings.warn("Softening spring (alpha < 0). The potential is unbounded below for large displacements. Global stability is not guaranteed.")

        self.m, self.b, self.k, self.alpha = m, b, k, alpha
        self.x0, self.v0 = x0, v0
        self.duration, self.num_samples = duration, num_samples
        self.forcing = forcing_function if forcing_function else ZeroForcing()

    def _ode_system(self, t: float, y: list) -> list:
        x, v = y
        F_ext = self.forcing(t)
        dxdt = v
        # Duffing Equation: m*x'' + b*x' + k*x + alpha*x^3 = F(t)
        dvdt = (F_ext - self.b * v - self.k * x - self.alpha * x**3) / self.m
        return [dxdt, dvdt]

    def simulate(self, y0: Optional[list] = None, rtol: float = 1e-8, atol: float = 1e-8, 
                 method: str = 'RK45') -> Dict[str, np.ndarray]:
        if y0 is None: y0 = [self.x0, self.v0]
        
        t_eval = np.linspace(0, self.duration, self.num_samples)
        sol = solve_ivp(self._ode_system, (0, self.duration), y0, t_eval=t_eval, 
                        method=method, rtol=rtol, atol=atol)
        
        t, x, v = sol.t, sol.y[0], sol.y[1]
        F_ext = np.array([self.forcing(ti) for ti in t])
        
        # Force and Energy Analysis
        F_linear = -self.k * x
        F_nonlinear = -self.alpha * x**3
        F_damping = -self.b * v
        F_net = F_linear + F_nonlinear + F_damping + F_ext
        
        K = 0.5 * self.m * v**2
        U_linear = 0.5 * self.k * x**2
        U_nonlinear = 0.25 * self.alpha * x**4
        E_tot = K + U_linear + U_nonlinear
        
        return {
            'time': t, 'x': x, 'v': v, 
            'F_linear': F_linear, 'F_nonlinear': F_nonlinear, 'F_damping': F_damping, 
            'F_ext': F_ext, 'F_net': F_net,
            'K': K, 'U_linear': U_linear, 'U_nonlinear': U_nonlinear, 'E_tot': E_tot
        }

def run_frequency_sweep(m=1.0, b=0.2, k=10.0, alpha=1.0, F0=2.0, 
                        w_min=1.0, w_max=6.0, steps=50, direction='forward') -> Dict[str, np.ndarray]:
    """Performs a continuation sweep to capture hysteresis and resonance bending."""
    omegas = np.linspace(w_min, w_max, steps)
    if direction == 'backward':
        omegas = np.flip(omegas)
        
    amplitudes = []
    current_y0 = [0.0, 0.0]
    
    for w in omegas:
        osc = DuffingOscillator(m, b, k, alpha, duration=50.0, num_samples=4000, 
                                forcing_function=SinusoidalForcing(F0, w))
        res = osc.simulate(y0=current_y0, rtol=1e-6, atol=1e-6)
        
        # Extract steady-state (last 20%)
        ss_idx = int(len(res['time']) * 0.8)
        x_ss = res['x'][ss_idx:]
        amp = (np.max(x_ss) - np.min(x_ss)) / 2.0
        amplitudes.append(amp)
        
        # Continuation: use final state as next initial condition
        current_y0 = [res['x'][-1], res['v'][-1]]
        
    if direction == 'backward':
        omegas = np.flip(omegas)
        amplitudes = np.flip(amplitudes)
        
    return {'omega': omegas, 'amplitude': np.array(amplitudes), 'direction': direction}


# --- Laboratory Visualizations ---

def plot_potential_and_force():
    x = np.linspace(-3, 3, 400)
    k = 10.0
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    
    for alpha, label, ls in zip([0.0, 2.0, -0.5], ['Linear ($\\alpha=0$)', 'Hardening ($\\alpha>0$)', 'Softening ($\\alpha<0$)'], ['-', '--', ':']):
        U = 0.5 * k * x**2 + 0.25 * alpha * x**4
        F = -k * x - alpha * x**3
        
        axs[0].plot(x, U, ls=ls, label=label, lw=2)
        axs[1].plot(x, F, ls=ls, label=label, lw=2)
        
    axs[0].set_title("Potential Energy $U(x)$"); axs[0].set_xlabel("Displacement $x$"); axs[0].set_ylabel("Energy (J)"); axs[0].grid(True); axs[0].set_ylim(-5, 50)
    axs[1].set_title("Restoring Force $F(x)$"); axs[1].set_xlabel("Displacement $x$"); axs[1].set_ylabel("Force (N)"); axs[1].grid(True); axs[1].legend()
    plt.tight_layout()
    plt.show()

def plot_sweep_comparison():
    print("Running nonlinear frequency sweeps (this may take a moment)...")
    sweep_fwd = run_frequency_sweep(alpha=2.0, direction='forward')
    sweep_bwd = run_frequency_sweep(alpha=2.0, direction='backward')
    
    # Linear reference
    sweep_lin = run_frequency_sweep(alpha=0.0, direction='forward')
    
    plt.figure(figsize=(10, 6))
    plt.plot(sweep_lin['omega'], sweep_lin['amplitude'], 'k-', label='Linear ($\\alpha=0$)')
    plt.plot(sweep_fwd['omega'], sweep_fwd['amplitude'], 'b^-', label='Hardening Forward Sweep', markersize=4)
    plt.plot(sweep_bwd['omega'], sweep_bwd['amplitude'], 'rv-', label='Hardening Backward Sweep', markersize=4)
    
    plt.title("Nonlinear Frequency Response (Jump Phenomenon & Hysteresis)")
    plt.xlabel("Driving Angular Frequency $\\omega$ (rad/s)")
    plt.ylabel("Steady-State Amplitude (m)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_harmonic_content():
    """Demonstrates generation of higher harmonics using FFT."""
    osc = DuffingOscillator(m=1.0, b=0.2, k=10.0, alpha=5.0, duration=100.0, num_samples=10000, 
                            forcing_function=SinusoidalForcing(F0=5.0, omega=2.0))
    res = osc.simulate()
    
    analyzer = SpectralAnalyzer(res['time'], res['x'])
    analyzer.remove_transient(cutoff_time=50.0)
    fft_res = analyzer.compute_fft(window='hann', pad_factor=4)
    
    plt.figure(figsize=(10, 5))
    plt.plot(fft_res['frequency_hz'], fft_res['amplitude'], 'b-')
    plt.xlim(0, 1.5)
    plt.yscale('log')
    plt.title("Harmonic Content of Duffing Oscillator (Log Scale)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    
    # Driving freq is 2.0 rad/s (~0.318 Hz). Odd harmonics at 3x, 5x...
    f_drive = 2.0 / (2 * np.pi)
    for i in [1, 3, 5]:
        plt.axvline(i * f_drive, color='r', linestyle='--', alpha=0.5, label=f'{i}x Harmonic' if i==1 else None)
        
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("--- Nonlinear Oscillators & Duffing Dynamics ---")
    plot_potential_and_force()
    plot_sweep_comparison()
    plot_harmonic_content()
