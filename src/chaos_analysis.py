"""
Milestone 12: Chaos Fundamentals & Poincaré Analysis Laboratory
Provides a computational foundation for identifying periodic vs. complex dynamics.
"""

import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from typing import Dict, List, Tuple

try:
    from nonlinear_oscillators import DuffingOscillator
    from forcing import SinusoidalForcing
    from spectral_analysis import SpectralAnalyzer
except ImportError:
    print("Warning: Prior milestone modules not found. Some features may be limited.")

class ChaosAnalyzer:
    def __init__(self, t: np.ndarray, x: np.ndarray, v: np.ndarray, omega_drive: float):
        self.t = t
        self.x = x
        self.v = v
        self.omega_drive = omega_drive
        self.T_drive = 2 * np.pi / omega_drive

    def remove_transient(self, transient_time: float):
        """Removes the early transient portion of the trajectory."""
        if transient_time >= self.t[-1]:
            raise ValueError("Transient time exceeds simulation duration.")
        idx = np.searchsorted(self.t, transient_time)
        self.t = self.t[idx:]
        self.x = self.x[idx:]
        self.v = self.v[idx:]

    def poincare_section(self, samples_per_drive_period: int = 1, phase_offset: float = 0.0) -> Dict[str, np.ndarray]:
        """Interpolates stroboscopic samples from the continuous trajectory."""
        t_min, t_max = self.t[0], self.t[-1]
        
        # Calculate sample times: t_n = t_0 + (n * T_drive / samples) + phase_offset
        first_sample = np.ceil(t_min / self.T_drive) * self.T_drive + phase_offset
        sample_times = np.arange(first_sample, t_max, self.T_drive / samples_per_drive_period)
        
        # Interpolate x and v precisely at the stroboscopic times
        x_interp = interp1d(self.t, self.x, kind='cubic')
        v_interp = interp1d(self.t, self.v, kind='cubic')
        
        px = x_interp(sample_times)
        pv = v_interp(sample_times)
        
        return {
            'sample_index': np.arange(len(sample_times)),
            'time': sample_times,
            'x': px,
            'v': pv
        }

    def detect_periodicity(self, px: np.ndarray, pv: np.ndarray, tol: float = 1e-2) -> Dict:
        """Clusters Poincaré points to estimate periodicity."""
        if len(px) < 2:
            return {'estimated_period': 0, 'classification': 'insufficient_data'}
            
        points = np.column_stack((px, pv))
        clusters = []
        
        for pt in points:
            matched = False
            for cluster in clusters:
                # Check Euclidean distance to existing cluster centers
                center = np.mean(cluster, axis=0)
                if np.linalg.norm(pt - center) < tol:
                    cluster.append(pt)
                    matched = True
                    break
            if not matched:
                clusters.append([pt])
                
        period = len(clusters)
        
        if period == 1: classification = "periodic_candidate"
        elif 1 < period <= 16: classification = "period_multiplied_candidate"
        else: classification = "complex_nonperiodic_candidate"
        
        return {
            'estimated_period': period,
            'cluster_count': period,
            'classification_confidence': 'diagnostic_only',
            'classification': classification
        }

    def recurrence_matrix(self, epsilon: float = 0.1) -> np.ndarray:
        """Constructs a binary recurrence matrix for the trajectory."""
        # Downsample slightly if trajectory is too large to prevent memory overflow
        max_points = 2000
        step = max(1, len(self.x) // max_points)
        x_ds, v_ds = self.x[::step], self.v[::step]
        
        points = np.column_stack((x_ds, v_ds))
        # Compute pairwise distances
        diffs = points[:, np.newaxis, :] - points[np.newaxis, :, :]
        distances = np.linalg.norm(diffs, axis=2)
        
        return (distances < epsilon).astype(int)

def sensitive_dependence_diagnostic(m=1.0, b=0.2, k=-1.0, alpha=1.0, F0=0.3, omega=1.2, 
                                    x0_1=0.0, v0_1=0.0, epsilon=1e-5):
    """Runs a paired simulation to measure finite-time trajectory separation."""
    forcing = SinusoidalForcing(F0, omega)
    
    # Trajectory 1
    osc1 = DuffingOscillator(m, b, k, alpha, duration=100.0, num_samples=10000, forcing_function=forcing)
    res1 = osc1.simulate(y0=[x0_1, v0_1], rtol=1e-9, atol=1e-9)
    
    # Trajectory 2 (Perturbed)
    osc2 = DuffingOscillator(m, b, k, alpha, duration=100.0, num_samples=10000, forcing_function=forcing)
    res2 = osc2.simulate(y0=[x0_1 + epsilon, v0_1], rtol=1e-9, atol=1e-9)
    
    # Calculate Separation
    dx = res1['x'] - res2['x']
    dv = res1['v'] - res2['v']
    separation = np.sqrt(dx**2 + dv**2)
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle("Sensitive Dependence Diagnostic (Not Definitive Proof of Chaos)")
    
    axs[0].plot(res1['time'], separation, 'k-')
    axs[0].set_ylabel("Separation Distance $d(t)$")
    axs[0].grid(True)
    
    axs[1].plot(res1['time'], np.log10(separation + 1e-16), 'b-')
    axs[1].set_ylabel("Log Separation $\log_{10} d(t)$")
    axs[1].set_xlabel("Time")
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()

def parameter_sweep_bifurcation(param_name='F0', param_range=(0.2, 0.4), steps=50):
    """Generates a Poincaré-based bifurcation visualization."""
    print(f"\nRunning Bifurcation Sweep for {param_name}...")
    param_vals = np.linspace(param_range[0], param_range[1], steps)
    bifurcation_data_x = []
    bifurcation_data_param = []
    
    # Fixed base parameters
    m, b, k, alpha, omega = 1.0, 0.2, -1.0, 1.0, 1.2 
    
    for val in param_vals:
        F0 = val if param_name == 'F0' else 0.3
        forcing = SinusoidalForcing(F0, omega)
        osc = DuffingOscillator(m, b, k, alpha, duration=200.0, num_samples=10000, forcing_function=forcing)
        res = osc.simulate(rtol=1e-7, atol=1e-7)
        
        analyzer = ChaosAnalyzer(res['time'], res['x'], res['v'], omega)
        analyzer.remove_transient(100.0) # Discard first 100 seconds
        poincare = analyzer.poincare_section()
        
        bifurcation_data_x.extend(poincare['x'])
        bifurcation_data_param.extend([val] * len(poincare['x']))

    plt.figure(figsize=(10, 6))
    plt.scatter(bifurcation_data_param, bifurcation_data_x, s=0.5, c='k', alpha=0.5)
    plt.title("Poincaré-Based Bifurcation Visualization")
    plt.xlabel(f"Control Parameter ({param_name})")
    plt.ylabel("Steady-State Poincaré Displacements $x_n$")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def run_experiment_preset(preset_path: str):
    """Loads and runs a JSON experiment preset."""
    with open(preset_path, 'r') as f:
        config = json.load(f)
        
    print(f"\n--- Running Preset: {os.path.basename(preset_path)} ---")
    forcing = SinusoidalForcing(config['F0'], config['omega'])
    osc = DuffingOscillator(config['m'], config['b'], config['k'], config['alpha'], 
                            duration=config['duration'], num_samples=15000, forcing_function=forcing)
    res = osc.simulate(y0=[config['x0'], config['v0']], rtol=1e-8, atol=1e-8)
    
    analyzer = ChaosAnalyzer(res['time'], res['x'], res['v'], config['omega'])
    analyzer.remove_transient(config['transient_time'])
    
    poincare = analyzer.poincare_section()
    diagnostics = analyzer.detect_periodicity(poincare['x'], poincare['v'])
    print(f"Classification: {diagnostics['classification']} (Estimated Period: {diagnostics['estimated_period']})")
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].plot(analyzer.x, analyzer.v, 'b-', lw=0.5, alpha=0.5)
    axs[0].set_title("Post-Transient Phase Space")
    axs[0].set_xlabel("Displacement"); axs[0].set_ylabel("Velocity"); axs[0].grid(True)
    
    axs[1].scatter(poincare['x'], poincare['v'], s=15, c='r')
    axs[1].set_title(f"Poincaré Section ($T_{{drive}} = {analyzer.T_drive:.2f}$)")
    axs[1].set_xlabel("Displacement"); axs[1].set_ylabel("Velocity"); axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()

def export_poincare_csv(poincare: Dict):
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'chaos'), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'chaos', 'poincare_section.csv')
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sample_index', 'time', 'x', 'v'])
        for i in range(len(poincare['time'])):
            writer.writerow([poincare['sample_index'][i], poincare['time'][i], poincare['x'][i], poincare['v'][i]])

if __name__ == "__main__":
    sensitive_dependence_diagnostic()
    parameter_sweep_bifurcation(param_name='F0', param_range=(0.25, 0.4))
