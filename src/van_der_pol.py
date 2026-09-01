"""
Milestone 11: Van der Pol Oscillator & Self-Sustained Oscillations
Analyzes limit cycles, nonlinear amplitude regulation, and relaxation oscillations.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks, correlate
from typing import Dict, List, Optional, Tuple

try:
    from forcing import ForcingFunction, ZeroForcing, SinusoidalForcing
    from spectral_analysis import SpectralAnalyzer
except ImportError:
    print("Warning: Prior milestone modules not found. Some features may be limited.")

class VanDerPolOscillator:
    def __init__(self, mu: float = 1.0, x0: float = 0.1, v0: float = 0.0, 
                 duration: float = 50.0, num_samples: int = 5000, 
                 forcing_function=None):
        """
        Dimensionless Van der Pol oscillator.
        x'' - mu*(1 - x^2)*x' + x = F(t)
        """
        if mu < 0:
            raise ValueError("Nonlinear damping parameter (mu) must be >= 0.")
        if duration <= 0 or num_samples <= 0:
            raise ValueError("Duration and num_samples must be positive.")

        self.mu = mu
        self.x0, self.v0 = x0, v0
        self.duration = duration
        self.num_samples = num_samples
        self.forcing = forcing_function if forcing_function else ZeroForcing()

    def _ode_system(self, t: float, y: list) -> list:
        x, v = y
        dxdt = v
        dvdt = self.mu * (1 - x**2) * v - x + self.forcing(t)
        return [dxdt, dvdt]

    def simulate(self, y0: Optional[list] = None, method: str = 'RK45', 
                 rtol: float = 1e-8, atol: float = 1e-8) -> Dict[str, np.ndarray]:
        if y0 is None: y0 = [self.x0, self.v0]
        
        t_eval = np.linspace(0, self.duration, self.num_samples)
        
        # BDF or Radau are recommended for stiff systems (large mu)
        sol = solve_ivp(self._ode_system, (0, self.duration), y0, t_eval=t_eval, 
                        method=method, rtol=rtol, atol=atol)
        
        t, x, v = sol.t, sol.y[0], sol.y[1]
        
        # Energy-like diagnostics (E_ref is NOT a conserved mechanical energy)
        E_ref = 0.5 * v**2 + 0.5 * x**2
        dE_ref_dt = self.mu * (1 - x**2) * v**2  # For unforced system
        
        return {
            'time': t, 'x': x, 'v': v, 
            'E_ref': E_ref, 'dE_ref_dt': dE_ref_dt
        }

def estimate_periodicity(t: np.ndarray, x: np.ndarray) -> Dict[str, float]:
    """Estimates period using zero-crossings, peaks, and autocorrelation."""
    dt = t[1] - t[0]
    
    # Peak detection
    peaks, _ = find_peaks(x)
    if len(peaks) > 1:
        peak_period = np.mean(np.diff(t[peaks]))
    else:
        peak_period = np.nan
        
    # Autocorrelation
    x_centered = x - np.mean(x)
    autocorr = correlate(x_centered, x_centered, mode='full')
    autocorr = autocorr[len(autocorr)//2:] # Take positive lags
    ac_peaks, _ = find_peaks(autocorr)
    
    if len(ac_peaks) > 0:
        ac_period = ac_peaks[0] * dt
    else:
        ac_period = np.nan
        
    return {
        'peak_period': peak_period,
        'autocorr_period': ac_period,
        'autocorr_array': autocorr
    }

def extract_limit_cycle_metrics(t: np.ndarray, x: np.ndarray, v: np.ndarray, 
                                dE_dt: np.ndarray, cutoff_fraction: float = 0.5) -> Dict[str, float]:
    """Analyzes the steady-state limit cycle after initial transients."""
    idx = int(len(t) * cutoff_fraction)
    x_lc, v_lc, dE_dt_lc = x[idx:], v[idx:], dE_dt[idx:]
    
    return {
        'max_amp': np.max(x_lc),
        'min_amp': np.min(x_lc),
        'rms_amp': np.sqrt(np.mean(x_lc**2)),
        'cycle_avg_dE_dt': np.mean(dE_dt_lc) # Should be ~0 for stable cycle
    }


# --- Laboratory Experiments & Visualizations ---

def run_limit_cycle_convergence():
    print("\n--- Limit Cycle Convergence Experiment ---")
    sys = VanDerPolOscillator(mu=1.0, duration=30.0, num_samples=3000)
    
    ics = [(0.1, 0.0), (3.0, 0.0), (-2.0, 3.0), (0.0, -4.0)]
    colors = ['r', 'b', 'g', 'm']
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Van der Pol Oscillator: Limit Cycle Attraction ($\mu=1.0$)")
    
    for (x0, v0), c in zip(ics, colors):
        res = sys.simulate(y0=[x0, v0])
        axs[0].plot(res['time'], res['x'], color=c, alpha=0.7, label=f'IC: ({x0}, {v0})')
        axs[1].plot(res['x'], res['v'], color=c, alpha=0.7, label=f'IC: ({x0}, {v0})')
        
    axs[0].set_title("Time Domain: Amplitude Regulation")
    axs[0].set_xlabel("Time"); axs[0].set_ylabel("Displacement $x$"); axs[0].grid(True)
    
    axs[1].set_title("Phase Space: Convergence to Stable Orbit")
    axs[1].set_xlabel("Displacement $x$"); axs[1].set_ylabel("Velocity $v$")
    axs[1].grid(True); axs[1].legend()
    
    plt.tight_layout()
    plt.show()

def run_mu_regimes_experiment():
    print("\n--- Van der Pol Regimes Experiment ---")
    mus = [0.1, 1.5, 5.0]
    titles = ["Small $\mu$ (Near-Sinusoidal)", "Moderate $\mu$ (Nonlinear)", "Large $\mu$ (Relaxation)"]
    
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle("Van der Pol Oscillator Dynamics Across $\mu$ Regimes")
    
    for i, (mu, title) in enumerate(zip(mus, titles)):
        sys = VanDerPolOscillator(mu=mu, duration=50.0, num_samples=5000)
        # Use BDF solver for stiff relaxation oscillations
        res = sys.simulate(y0=[2.0, 0.0], method='BDF' if mu > 2.0 else 'RK45')
        metrics = extract_limit_cycle_metrics(res['time'], res['x'], res['v'], res['dE_ref_dt'])
        period = estimate_periodicity(res['time'], res['x'])['peak_period']
        
        axs[i, 0].plot(res['time'][-2000:], res['x'][-2000:], 'b-')
        axs[i, 0].set_title(f"{title} - Time Domain (T $\\approx$ {period:.2f})")
        axs[i, 0].set_ylabel("Displacement $x$"); axs[i, 0].grid(True)
        
        axs[i, 1].plot(res['x'][-2000:], res['v'][-2000:], 'r-')
        axs[i, 1].set_title(f"Phase Space Limit Cycle")
        axs[i, 1].set_ylabel("Velocity $v$"); axs[i, 1].grid(True)
        
        print(f"mu={mu}: Cycle-Avg dE_ref/dt = {metrics['cycle_avg_dE_dt']:.2e}, Period = {period:.2f}")

    axs[2, 0].set_xlabel("Time")
    axs[2, 1].set_xlabel("Displacement $x$")
    plt.tight_layout()
    plt.show()

def run_energy_balance_experiment():
    print("\n--- Energy-Like Diagnostics Experiment ---")
    sys = VanDerPolOscillator(mu=1.0, duration=20.0, num_samples=2000)
    res = sys.simulate(y0=[0.1, 0.0]) # Start small to show growth
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("Van der Pol Energy-Like Behavior ($\mu=1.0$)")
    
    axs[0].plot(res['time'], res['E_ref'], 'g-', label='$E_{ref} = 0.5 v^2 + 0.5 x^2$')
    axs[0].set_title("Energy-Like Quantity (Growth to Saturation)")
    axs[0].set_ylabel("$E_{ref}$"); axs[0].legend(); axs[0].grid(True)
    
    axs[1].plot(res['time'], res['dE_ref_dt'], 'k-', label='$dE_{ref}/dt$')
    axs[1].axhline(0, color='r', linestyle='--')
    axs[1].fill_between(res['time'], 0, res['dE_ref_dt'], where=(res['dE_ref_dt'] > 0), color='blue', alpha=0.3, label='Energy Growth ($|x| < 1$)')
    axs[1].fill_between(res['time'], 0, res['dE_ref_dt'], where=(res['dE_ref_dt'] < 0), color='red', alpha=0.3, label='Energy Dissipation ($|x| > 1$)')
    
    axs[1].set_title("Rate of Energy Change (Cycle Average approaches 0)")
    axs[1].set_xlabel("Time"); axs[1].set_ylabel("Rate"); axs[1].legend(loc='lower right'); axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()

def export_van_der_pol_csv():
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'van_der_pol'), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'van_der_pol', 'simulation.csv')
    
    sys = VanDerPolOscillator(mu=2.0)
    res = sys.simulate()
    
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'displacement', 'velocity', 'energy_reference', 'energy_rate'])
        for i in range(len(res['time'])):
            writer.writerow([
                res['time'][i], res['x'][i], res['v'][i], res['E_ref'][i], res['dE_ref_dt'][i]
            ])
    print("\nData exported to results/van_der_pol/simulation.csv")

if __name__ == "__main__":
    run_limit_cycle_convergence()
    run_mu_regimes_experiment()
    run_energy_balance_experiment()
    export_van_der_pol_csv()
