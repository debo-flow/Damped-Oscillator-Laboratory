"""
Milestone 9: Coupled Oscillators & Normal Modes Laboratory
Simulates two coupled harmonic oscillators, solves for normal modes, 
and analyzes energy transfer and beating phenomena.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.linalg import eigh
from typing import Dict, Tuple, List

# Reuse the FFT analyzer from Milestone 8
try:
    from spectral_analysis import SpectralAnalyzer
except ImportError:
    print("Warning: spectral_analysis module not found. FFT features will be limited.")

class CoupledOscillators:
    def __init__(self, m1=1.0, m2=1.0, k1=10.0, k2=10.0, kc=2.0, b1=0.0, b2=0.0):
        if m1 <= 0 or m2 <= 0: raise ValueError("Masses must be positive.")
        if k1 <= 0 or k2 <= 0: raise ValueError("Grounding spring constants must be positive.")
        if kc < 0: raise ValueError("Coupling spring constant must be non-negative.")
        if b1 < 0 or b2 < 0: raise ValueError("Damping coefficients must be non-negative.")
        
        self.m1, self.m2 = m1, m2
        self.k1, self.k2, self.kc = k1, k2, kc
        self.b1, self.b2 = b1, b2

    def get_matrices(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Constructs the M, C, and K matrices for the system."""
        M = np.array([[self.m1, 0], 
                      [0, self.m2]])
        C = np.array([[self.b1, 0], 
                      [0, self.b2]])
        K = np.array([[self.k1 + self.kc, -self.kc], 
                      [-self.kc,          self.k2 + self.kc]])
        return M, C, K

    def solve_eigenproblem(self) -> Dict:
        """Solves the generalized eigenvalue problem K*u = w^2*M*u for undamped normal modes."""
        M, _, K = self.get_matrices()
        eigenvalues, eigenvectors = eigh(K, M)
        
        # Sort in ascending frequency order
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        omega = np.sqrt(eigenvalues)
        
        # Normalize eigenvectors (max displacement = 1) for clear mode shape readability
        for i in range(2):
            max_idx = np.argmax(np.abs(eigenvectors[:, i]))
            eigenvectors[:, i] /= eigenvectors[max_idx, i]
            
        return {
            'eigenvalues': eigenvalues,
            'omega': omega,
            'freq_hz': omega / (2 * np.pi),
            'mode_shapes': eigenvectors
        }

    def _ode_system(self, t: float, y: list) -> list:
        x1, v1, x2, v2 = y
        dx1dt = v1
        dv1dt = (-self.k1*x1 - self.kc*(x1 - x2) - self.b1*v1) / self.m1
        dx2dt = v2
        dv2dt = (-self.k2*x2 - self.kc*(x2 - x1) - self.b2*v2) / self.m2
        return [dx1dt, dv1dt, dx2dt, dv2dt]

    def simulate(self, y0: list, duration: float = 20.0, num_samples: int = 2000, 
                 rtol: float = 1e-8, atol: float = 1e-8) -> Dict[str, np.ndarray]:
        t_eval = np.linspace(0, duration, num_samples)
        sol = solve_ivp(self._ode_system, (0, duration), y0, t_eval=t_eval, method='RK45', rtol=rtol, atol=atol)
        
        t = sol.t
        x1, v1, x2, v2 = sol.y
        
        return {'time': t, 'x1': x1, 'v1': v1, 'x2': x2, 'v2': v2}

    def analyze_energy(self, res: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Calculates kinetic, potential, and subsystem energies."""
        x1, v1, x2, v2 = res['x1'], res['v1'], res['x2'], res['v2']
        
        K1 = 0.5 * self.m1 * v1**2
        K2 = 0.5 * self.m2 * v2**2
        Ug1 = 0.5 * self.k1 * x1**2
        Ug2 = 0.5 * self.k2 * x2**2
        Uc = 0.5 * self.kc * (x1 - x2)**2
        
        E_tot = K1 + K2 + Ug1 + Ug2 + Uc
        # Subsystem energies (convention: equally split coupling energy)
        E_osc1 = K1 + Ug1 + 0.5 * Uc
        E_osc2 = K2 + Ug2 + 0.5 * Uc
        
        return {
            'K1': K1, 'K2': K2, 'Ug1': Ug1, 'Ug2': Ug2, 'Uc': Uc,
            'E_tot': E_tot, 'E_osc1': E_osc1, 'E_osc2': E_osc2
        }


# --- Laboratory Experiments & Visualizations ---

def run_beating_experiment():
    print("\n--- Beating & Weak Coupling Experiment ---")
    # Identical masses, weak coupling (kc << k1)
    sys = CoupledOscillators(m1=1.0, m2=1.0, k1=10.0, k2=10.0, kc=0.5)
    modes = sys.solve_eigenproblem()
    
    print(f"Normal Mode 1 (Symmetric): {modes['omega'][0]:.4f} rad/s")
    print(f"Normal Mode 2 (Antisym):   {modes['omega'][1]:.4f} rad/s")
    
    w_beat = np.abs(modes['omega'][1] - modes['omega'][0])
    print(f"Theoretical Beat Freq:     {w_beat/(2*np.pi):.4f} Hz")
    
    # Excite Oscillator 1 only to trigger beating
    res = sys.simulate([1.0, 0.0, 0.0, 0.0], duration=50.0, num_samples=5000)
    en = sys.analyze_energy(res)
    
    # FFT Analysis
    analyzer = SpectralAnalyzer(res['time'], res['x1'])
    fft_res = analyzer.compute_fft(window='hann', pad_factor=4)
    
    export_coupled_csv("weak_coupling_beating", res, en)
    
    # 1. Beating Displacement Plot
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    fig.suptitle("Weak Coupling: Beating Phenomenon", fontsize=16)
    
    axs[0].plot(res['time'], res['x1'], 'b-', label='Oscillator 1 ($x_1$)')
    axs[0].plot(res['time'], res['x2'], 'r-', alpha=0.7, label='Oscillator 2 ($x_2$)')
    axs[0].set_ylabel("Displacement (m)")
    axs[0].legend(loc='upper right')
    axs[0].grid(True)
    
    # 2. Energy Transfer Plot
    axs[1].plot(res['time'], en['E_osc1'], 'b-', label='Energy Osc 1')
    axs[1].plot(res['time'], en['E_osc2'], 'r-', label='Energy Osc 2')
    axs[1].plot(res['time'], en['E_tot'], 'k--', label='Total Energy')
    axs[1].set_ylabel("Energy (J)")
    axs[1].legend(loc='upper right')
    axs[1].grid(True)
    
    # 3. FFT Plot showing split peaks
    axs[2].plot(fft_res['frequency_hz'], fft_res['amplitude'], 'g-')
    axs[2].axvline(modes['freq_hz'][0], color='k', linestyle='--', label=f"Mode 1 ({modes['freq_hz'][0]:.3f} Hz)")
    axs[2].axvline(modes['freq_hz'][1], color='m', linestyle='--', label=f"Mode 2 ({modes['freq_hz'][1]:.3f} Hz)")
    axs[2].set_xlim(0, 1.5)
    axs[2].set_xlabel("Frequency (Hz)")
    axs[2].set_ylabel("Amplitude")
    axs[2].legend()
    axs[2].grid(True)
    
    plt.tight_layout()
    plt.show()

def run_normal_modes_experiment():
    print("\n--- Normal Modes Phase-Space Experiment ---")
    sys = CoupledOscillators(m1=1.0, m2=1.0, k1=10.0, k2=10.0, kc=2.0)
    
    # Symmetric IC
    res_sym = sys.simulate([1.0, 0.0, 1.0, 0.0], duration=10.0)
    # Antisymmetric IC
    res_anti = sys.simulate([1.0, 0.0, -1.0, 0.0], duration=10.0)
    # Mixed IC
    res_mix = sys.simulate([1.0, 0.0, 0.0, 0.0], duration=10.0)

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Coupled Phase Space ($x_1$ vs $x_2$)", fontsize=16)
    
    axs[0].plot(res_sym['x1'], res_sym['x2'], 'b-')
    axs[0].set_title("Symmetric Mode Initialization\n($x_1 = x_2$)")
    
    axs[1].plot(res_anti['x1'], res_anti['x2'], 'r-')
    axs[1].set_title("Antisymmetric Mode Initialization\n($x_1 = -x_2$)")
    
    axs[2].plot(res_mix['x1'], res_mix['x2'], 'g-')
    axs[2].set_title("Mixed Superposition Initialization\n(Lissajous Figure)")
    
    for ax in axs:
        ax.set_xlabel("Oscillator 1 Displacement ($x_1$)")
        ax.set_ylabel("Oscillator 2 Displacement ($x_2$)")
        ax.axhline(0, color='k', lw=0.5); ax.axvline(0, color='k', lw=0.5)
        ax.grid(True)
        ax.set_aspect('equal')
        
    plt.tight_layout()
    plt.show()

def export_coupled_csv(name: str, res: Dict, en: Dict):
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'coupled'), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'coupled', f'{name}.csv')
    
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'x1', 'v1', 'x2', 'v2', 'K1', 'K2', 'Uc', 'E_osc1', 'E_osc2', 'E_tot'])
        for i in range(len(res['time'])):
            writer.writerow([
                res['time'][i], res['x1'][i], res['v1'][i], res['x2'][i], res['v2'][i],
                en['K1'][i], en['K2'][i], en['Uc'][i], en['E_osc1'][i], en['E_osc2'][i], en['E_tot'][i]
            ])

if __name__ == "__main__":
    run_beating_experiment()
    run_normal_modes_experiment()

