"""
Milestone 7: Resonance & Frequency Response Laboratory
Analyzes the steady-state frequency response, resonance, and bandwidth of the forced oscillator.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from typing import Dict, Tuple, Optional, List
from damped_oscillator import DampedOscillator
from forcing import SinusoidalForcing
from energy_analysis import EnergyAnalyzer

class ResonanceAnalyzer:
    def __init__(self, m: float, b: float, k: float):
        if m <= 0 or k <= 0 or b < 0:
            raise ValueError("Invalid physical parameters.")
        self.m, self.b, self.k = m, b, k
        self.w0 = np.sqrt(k / m)
        self.zeta = b / (2 * np.sqrt(m * k))

    def theoretical_amplitude(self, omega: np.ndarray, F0: float = 1.0) -> np.ndarray:
        """X(w) = F0 / sqrt((k - m*w^2)^2 + (b*w)^2)"""
        # Handle b=0 singularity warning at w = w0
        if self.b == 0 and np.any(np.isclose(omega, self.w0)):
            import warnings
            warnings.warn("Undamped system (b=0) exhibits infinite amplitude at resonance.")
        denominator = np.sqrt((self.k - self.m * omega**2)**2 + (self.b * omega)**2)
        return F0 / denominator

    def theoretical_phase(self, omega: np.ndarray) -> np.ndarray:
        """phi(w) = atan2(b*w, k - m*w^2)"""
        return np.arctan2(self.b * omega, self.k - self.m * omega**2)

    def resonance_frequency(self) -> Optional[float]:
        """w_r = w0 * sqrt(1 - 2*zeta^2) if zeta < 1/sqrt(2), else None"""
        if self.zeta < 1 / np.sqrt(2):
            return self.w0 * np.sqrt(1 - 2 * self.zeta**2)
        return None

    def quality_factor_theoretical(self) -> float:
        """Q = m * w0 / b"""
        if self.b == 0:
            return np.inf
        return (self.m * self.w0) / self.b

    def frequency_sweep(self, f_min: float, f_max: float, num_points: int = 1000, 
                        mode: str = 'linear', F0: float = 1.0) -> Dict[str, np.ndarray]:
        """Performs a frequency sweep and calculates theoretical responses."""
        if mode == 'log':
            w = np.logspace(np.log10(f_min), np.log10(f_max), num_points)
        else:
            w = np.linspace(f_min, f_max, num_points)
            
        amp = self.theoretical_amplitude(w, F0)
        phase_rad = self.theoretical_phase(w)
        
        return {
            'omega': w,
            'f_hz': w / (2 * np.pi),
            'amplitude': amp,
            'normalized_amplitude': amp / (F0 / self.k),  # X(w) / X(0)
            'phase_rad': phase_rad,
            'phase_deg': np.degrees(phase_rad)
        }

    def refine_resonance(self, sweep: Dict[str, np.ndarray], F0: float = 1.0) -> Dict[str, float]:
        """Locates the numerical peak and calculates bandwidth and Q via interpolation."""
        amp = sweep['amplitude']
        w = sweep['omega']
        
        max_idx = np.argmax(amp)
        w_r_num = w[max_idx]
        amp_max = amp[max_idx]
        
        # Bandwidth calculation
        half_power_amp = amp_max / np.sqrt(2)
        
        try:
            # Interpolate strictly on the left and right slopes of the peak
            left_interp = interp1d(amp[:max_idx], w[:max_idx])
            right_interp = interp1d(amp[max_idx:], w[max_idx:])
            
            w1 = float(left_interp(half_power_amp))
            w2 = float(right_interp(half_power_amp))
            bw = w2 - w1
            Q_num = w_r_num / bw
        except ValueError:
            # Occurs if half-power points fall outside the sweep range
            w1, w2, bw, Q_num = None, None, None, None

        return {
            'w_r_num': w_r_num,
            'amp_max': amp_max,
            'w1': w1,
            'w2': w2,
            'bandwidth': bw,
            'Q_num': Q_num
        }

    def validate_time_domain_energy(self, omega: float, F0: float = 1.0) -> Dict[str, float]:
        """Runs the time-domain simulator to average power and extract steady state."""
        forcing = SinusoidalForcing(F0, omega)
        osc = DampedOscillator(self.m, self.b, self.k, duration=50.0, num_samples=5000, forcing_function=forcing)
        res = osc.simulate(rtol=1e-7, atol=1e-7)
        
        ea = EnergyAnalyzer(self.m, self.b, self.k)
        en = ea.compute_energy_dynamics(res['time'], res['displacement'], res['velocity'], res['external_force'])
        
        # Extract steady state (last 20% of the simulation)
        ss_idx = int(len(res['time']) * 0.8)
        x_ss = res['displacement'][ss_idx:]
        
        # Numerical Amplitude
        num_amp = (np.max(x_ss) - np.min(x_ss)) / 2.0
        
        # Average Powers in Steady State
        avg_p_drive = np.mean(en['P_drive'][ss_idx:])
        avg_p_diss = np.mean(en['P_d'][ss_idx:])  # P_d is negative
        
        return {
            'num_amplitude': num_amp,
            'avg_p_drive': avg_p_drive,
            'avg_p_diss': avg_p_diss,
            'power_balance_error': np.abs(avg_p_drive + avg_p_diss)
        }

def plot_resonance_suite(m=1.0, b=0.2, k=10.0, F0=1.0):
    analyzer = ResonanceAnalyzer(m, b, k)
    sweep = analyzer.frequency_sweep(0.1, 10.0, 2000)
    metrics = analyzer.refine_resonance(sweep, F0)
    w_0 = analyzer.w0
    w_r = analyzer.resonance_frequency()

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Frequency Response Laboratory (m={m}, b={b}, k={k})", fontsize=16)

    # 1. Amplitude vs Angular Frequency
    axs[0, 0].plot(sweep['omega'], sweep['amplitude'], 'b-', lw=2)
    axs[0, 0].axvline(w_0, color='k', linestyle='--', label='$\omega_0$ (Natural)')
    if w_r: axs[0, 0].axvline(w_r, color='r', linestyle='--', label='$\omega_r$ (Resonance)')
    if metrics['w1'] and metrics['w2']:
        axs[0, 0].axvspan(metrics['w1'], metrics['w2'], color='gray', alpha=0.2, label='Bandwidth ($\Delta\omega$)')
    axs[0, 0].set_xlabel("Angular Frequency $\omega$ (rad/s)")
    axs[0, 0].set_ylabel("Amplitude (m)")
    axs[0, 0].set_title("Amplitude Response")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Amplitude vs Frequency (Hz)
    axs[0, 1].plot(sweep['f_hz'], sweep['amplitude'], 'g-', lw=2)
    axs[0, 1].set_xlabel("Frequency $f$ (Hz)")
    axs[0, 1].set_ylabel("Amplitude (m)")
    axs[0, 1].set_title("Amplitude Response (Hz)")
    axs[0, 1].grid(True)

    # 3. Phase vs Angular Frequency
    axs[1, 0].plot(sweep['omega'], sweep['phase_deg'], 'r-', lw=2)
    axs[1, 0].axvline(w_0, color='k', linestyle='--')
    axs[1, 0].set_xlabel("Angular Frequency $\omega$ (rad/s)")
    axs[1, 0].set_ylabel("Phase Lag (degrees)")
    axs[1, 0].set_title("Phase Response")
    axs[1, 0].grid(True)

    # 4. Normalized Amplitude vs Frequency Ratio
    w_ratio = sweep['omega'] / w_0
    axs[1, 1].plot(w_ratio, sweep['normalized_amplitude'], 'purple', lw=2)
    axs[1, 1].set_xlabel("Frequency Ratio ($\omega / \omega_0$)")
    axs[1, 1].set_ylabel("Normalized Amplitude $X(\omega)/X(0)$")
    axs[1, 1].set_title("Normalized Response")
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()

def plot_damping_comparison():
    b_values = [0.2, 1.0, 5.0]
    colors = ['r', 'g', 'b']
    labels = ['Light ($b=0.2$)', 'Moderate ($b=1.0$)', 'Strong ($b=5.0$)']
    
    plt.figure(figsize=(10, 6))
    for b, c, l in zip(b_values, colors, labels):
        analyzer = ResonanceAnalyzer(m=1.0, b=b, k=10.0)
        sweep = analyzer.frequency_sweep(0.1, 10.0, 2000)
        plt.plot(sweep['omega'], sweep['amplitude'], color=c, lw=2, label=l)
    
    plt.axvline(np.sqrt(10), color='k', linestyle='--', label='$\omega_0$ (Natural)')
    plt.title("Resonance Curves Across Damping Regimes")
    plt.xlabel("Angular Frequency $\omega$ (rad/s)")
    plt.ylabel("Amplitude (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def export_resonance_data(analyzer: ResonanceAnalyzer, sweep: Dict, metrics: Dict):
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'resonance'), exist_ok=True)
    
    # 1. Frequency Response Sweep
    sweep_file = os.path.join(os.path.dirname(__file__), '..', 'results', 'resonance', 'frequency_response.csv')
    with open(sweep_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['omega', 'f_hz', 'amplitude', 'phase_rad', 'phase_deg', 'normalized_amplitude'])
        for i in range(len(sweep['omega'])):
            writer.writerow([
                sweep['omega'][i], sweep['f_hz'][i], sweep['amplitude'][i],
                sweep['phase_rad'][i], sweep['phase_deg'][i], sweep['normalized_amplitude'][i]
            ])
            
    # 2. Resonance Summary
    summary_file = os.path.join(os.path.dirname(__file__), '..', 'results', 'resonance', 'resonance_summary.csv')
    with open(summary_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['m', 'b', 'k', 'zeta', 'w0', 'w_r_theo', 'w_r_num', 'amp_max', 'w1', 'w2', 'bw', 'Q_theo', 'Q_num'])
        writer.writerow([
            analyzer.m, analyzer.b, analyzer.k, analyzer.zeta, analyzer.w0,
            analyzer.resonance_frequency(), metrics['w_r_num'], metrics['amp_max'],
            metrics['w1'], metrics['w2'], metrics['bandwidth'],
            analyzer.quality_factor_theoretical(), metrics['Q_num']
        ])

if __name__ == "__main__":
    print("--- Resonance & Frequency Response Laboratory ---")
    analyzer = ResonanceAnalyzer(m=1.0, b=0.2, k=10.0)
    
    print("\nRunning Time-Domain Validation (Energy Balance)...")
    # Test near resonance
    val = analyzer.validate_time_domain_energy(omega=3.16, F0=1.0)
    print(f"Num Amplitude: {val['num_amplitude']:.4f} m")
    print(f"Avg P_drive:   {val['avg_p_drive']:.4f} W")
    print(f"Avg P_diss:    {val['avg_p_diss']:.4f} W")
    print(f"Power Balance Error: {val['power_balance_error']:.2e} W")
    
    print("\nGenerating Plots...")
    plot_resonance_suite(m=1.0, b=0.2, k=10.0)
    plot_damping_comparison()
    
    print("\nExporting Data...")
    sweep = analyzer.frequency_sweep(0.1, 10.0, 2000)
    metrics = analyzer.refine_resonance(sweep)
    export_resonance_data(analyzer, sweep, metrics)
    print("Export Complete.")

