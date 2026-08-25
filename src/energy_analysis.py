"""
Milestone 5: Energy Dynamics & Dissipation Laboratory
Analyzes mechanical energy, power loss, and energy balance residuals.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from typing import Dict, Any
from damped_oscillator import DampedOscillator

class EnergyAnalyzer:
    def __init__(self, m: float, b: float, k: float):
        self.m = m
        self.b = b
        self.k = k

    def compute_energy_dynamics(self, t: np.ndarray, x: np.ndarray, v: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculates energy, power, forces, and dissipation metrics."""
        # 1. Fundamental Energy Components
        K = 0.5 * self.m * v**2
        U = 0.5 * self.k * x**2
        E = K + U
        
        # 2. Forces
        F_s = -self.k * x
        F_d = -self.b * v
        F_tot = F_s + F_d

        # 3. Power and Theoretical Derivatives
        P_d = -self.b * v**2  # Signed damping power (always <= 0)
        
        # Numerical Derivative of E (using central differences where possible)
        dE_dt_num = np.gradient(E, t)
        
        # 4. Energy Dissipation & Balance
        # Dissipated energy = integral of (b * v^2) dt
        P_diss_mag = self.b * v**2
        E_diss = cumulative_trapezoid(P_diss_mag, t, initial=0.0)
        
        # Residual: E(0) - E(t) - E_diss(t)
        E_0 = E[0]
        R_E = E_0 - E - E_diss
        
        return {
            'time': t, 'K': K, 'U': U, 'E': E,
            'F_s': F_s, 'F_d': F_d, 'F_tot': F_tot,
            'P_d': P_d, 'dE_dt_num': dE_dt_num,
            'E_diss': E_diss, 'R_E': R_E
        }

    def calculate_metrics(self, data: Dict[str, np.ndarray]) -> Dict[str, float]:
        """Calculates quantitative metrics for energy balance accuracy."""
        R_E = data['R_E']
        P_d = data['P_d']
        dE_dt_num = data['dE_dt_num']
        
        # Power equation error: |(dE/dt)_num - P_d|
        e_P = np.abs(dE_dt_num - P_d)
        
        return {
            'max_R_E': np.max(np.abs(R_E)),
            'rms_R_E': np.sqrt(np.mean(R_E**2)),
            'max_e_P': np.max(e_P),
            'rms_e_P': np.sqrt(np.mean(e_P**2))
        }


def plot_energy_suite(name: str, data: Dict[str, np.ndarray]):
    """Generates the 5 required energy analysis plots."""
    t = data['time']
    
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))
    fig.suptitle(f"Energy Dynamics Laboratory: {name}", fontsize=16)

    # Plot 1: Energy Components
    axs[0, 0].plot(t, data['K'], label='Kinetic Energy ($K$)')
    axs[0, 0].plot(t, data['U'], label='Potential Energy ($U$)')
    axs[0, 0].plot(t, data['E'], 'k--', lw=2, label='Total Mechanical ($E$)')
    axs[0, 0].set_title("Energy Components vs Time")
    axs[0, 0].set_ylabel("Energy (J)")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot 2: Energy Dissipation
    axs[0, 1].plot(t, data['E_diss'], 'r-', label='Dissipated Energy ($E_{diss}$)')
    axs[0, 1].plot(t, data['E'], 'k-', label='Remaining Energy ($E$)')
    axs[0, 1].set_title("Energy Dissipation vs Time")
    axs[0, 1].set_ylabel("Energy (J)")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot 3: Damping Power
    axs[1, 0].plot(t, data['P_d'], 'b-')
    axs[1, 0].set_title("Damping Power vs Time")
    axs[1, 0].set_ylabel("Power (W)")
    axs[1, 0].grid(True)

    # Plot 4: Energy-Balance Residual
    axs[1, 1].plot(t, data['R_E'], 'g-')
    axs[1, 1].set_title("Energy-Balance Residual ($R_E$)")
    axs[1, 1].set_ylabel("Error (J)")
    axs[1, 1].set_yscale('symlog', linthresh=1e-12)
    axs[1, 1].grid(True)

    # Plot 5: Force Analysis
    axs[2, 0].plot(t, data['F_s'], label='Spring Force ($F_s$)')
    axs[2, 0].plot(t, data['F_d'], label='Damping Force ($F_d$)')
    axs[2, 0].plot(t, data['F_tot'], 'k--', label='Total Internal Force')
    axs[2, 0].set_title("Internal Forces vs Time")
    axs[2, 0].set_ylabel("Force (N)")
    axs[2, 0].set_xlabel("Time (s)")
    axs[2, 0].legend()
    axs[2, 0].grid(True)

    # Hide the empty 6th subplot
    axs[2, 1].axis('off')
    
    plt.tight_layout()
    plt.show()

def plot_energy_phase_space(name: str, x: np.ndarray, v: np.ndarray, E: np.ndarray):
    """Plots the phase-space trajectory colored by instantaneous mechanical energy."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    scatter = ax.scatter(x, v, c=E, cmap='plasma', s=3, label='Trajectory')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Mechanical Energy (J)')
    
    ax.set_title(f"Energy-Colored Phase Space: {name}")
    ax.set_xlabel("Displacement (m)")
    ax.set_ylabel("Velocity (m/s)")
    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def export_energy_csv(name: str, data: Dict[str, np.ndarray]):
    """Exports the calculated energy dynamics to a CSV file."""
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'energy'), exist_ok=True)
    filename = os.path.join(os.path.dirname(__file__), '..', 'results', 'energy', f'{name.lower().replace(" ", "_")}_energy.csv')
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'K', 'U', 'E', 'F_s', 'F_d', 'P_d', 'E_diss', 'R_E'])
        for i in range(len(data['time'])):
            writer.writerow([
                data['time'][i], data['K'][i], data['U'][i], data['E'][i],
                data['F_s'][i], data['F_d'][i], data['P_d'][i], 
                data['E_diss'][i], data['R_E'][i]
            ])

def run_energy_convergence_study():
    """Runs the energy balance equation with progressively stricter settings."""
    m, b, k = 1.0, 0.5, 10.0
    print("\n--- Energy Balance Convergence Study ---")
    print(f"{'Tolerance':<12} | {'Max R_E (J)':<15} | {'RMS R_E (J)'}")
    print("-" * 45)
    
    osc = DampedOscillator(m, b, k, x0=1.0, v0=0.0, duration=10)
    analyzer = EnergyAnalyzer(m, b, k)
    
    for tol in [1e-3, 1e-5, 1e-7, 1e-9]:
        res = osc.simulate(rtol=tol, atol=tol*1e-3)
        energy_data = analyzer.compute_energy_dynamics(res['time'], res['displacement'], res['velocity'])
        metrics = analyzer.calculate_metrics(energy_data)
        
        print(f"{tol:<12.0e} | {metrics['max_R_E']:<15.3e} | {metrics['rms_R_E']:.3e}")


def run_regime(name: str, m: float, b: float, k: float):
    print(f"\nAnalyzing Energy Dynamics: {name}")
    osc = DampedOscillator(m, b, k, x0=1.0, v0=0.0, duration=15, num_samples=2000)
    analyzer = EnergyAnalyzer(m, b, k)
    
    res = osc.simulate(rtol=1e-8, atol=1e-8)
    energy_data = analyzer.compute_energy_dynamics(res['time'], res['displacement'], res['velocity'])
    
    export_energy_csv(name, energy_data)
    plot_energy_suite(name, energy_data)
    plot_energy_phase_space(name, res['displacement'], res['velocity'], energy_data['E'])


if __name__ == "__main__":
    run_energy_convergence_study()
    run_regime("Underdamped", m=1.0, b=0.5, k=10.0)
    run_regime("Critically Damped", m=1.0, b=2*np.sqrt(10.0), k=10.0)
    run_regime("Overdamped", m=1.0, b=10.0, k=10.0)
