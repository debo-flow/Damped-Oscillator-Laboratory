"""
Milestone 6: Forced Damped Oscillator Laboratory
Simulates and visualizes the response of an oscillator to periodic external forcing.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from damped_oscillator import DampedOscillator
from forcing import SinusoidalForcing
from analytical_solution import AnalyticalSolver
from energy_analysis import EnergyAnalyzer

def run_forced_experiment():
    m, b, k = 1.0, 0.5, 10.0
    F0, omega = 1.0, 2.0
    x0, v0 = 0.0, 0.0
    t_max = 30.0 # Long enough to see steady-state
    
    print("\n--- Forced Oscillator Laboratory ---")
    
    # Setup numerical
    forcing = SinusoidalForcing(F0, omega)
    osc = DampedOscillator(m, b, k, x0, v0, duration=t_max, num_samples=3000, forcing_function=forcing)
    num_res = osc.simulate(rtol=1e-8, atol=1e-8)
    
    # Setup analytical
    ana = AnalyticalSolver(m, b, k, x0, v0, F0=F0, omega_f=omega)
    ana_res = ana.solve(num_res['time'])
    
    # Energy
    ea = EnergyAnalyzer(m, b, k)
    en_res = ea.compute_energy_dynamics(num_res['time'], num_res['displacement'], num_res['velocity'], num_res['external_force'])
    
    # Analysis & Print
    t_steady = t_max * 0.8  # Assume last 20% is steady state
    steady_idx = num_res['time'] > t_steady
    
    max_err = np.max(np.abs(num_res['displacement'] - ana_res['displacement']))
    num_amp = np.max(np.abs(num_res['displacement'][steady_idx]))
    
    print(f"Theoretical Amplitude: {ana_res['amplitude']:.4f} m")
    print(f"Numerical Amplitude:   {num_amp:.4f} m")
    print(f"Theoretical Phase:     {ana_res['phase']:.4f} rad")
    print(f"Max Global Error:      {max_err:.3e} m")
    
    export_forced_csv(num_res, ana_res, en_res)
    plot_time_domain(num_res, ana_res)
    plot_transient_vs_steady(ana_res)
    plot_forced_phase_space(osc, forcing)


def plot_time_domain(num, ana):
    t = num['time']
    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    
    axs[0].plot(t, num['external_force'], 'g-', label='$F_{drive}(t)$')
    axs[0].set_ylabel("Force (N)")
    axs[0].set_title("External Driving Force")
    axs[0].legend(); axs[0].grid(True)
    
    axs[1].plot(t, ana['displacement'], 'k-', lw=3, alpha=0.5, label='Analytical')
    axs[1].plot(t, num['displacement'], 'r--', label='Numerical')
    axs[1].set_ylabel("Displacement (m)")
    axs[1].set_title("Displacement vs Time")
    axs[1].legend(); axs[1].grid(True)
    
    axs[2].plot(t, ana['velocity'], 'k-', lw=3, alpha=0.5, label='Analytical')
    axs[2].plot(t, num['velocity'], 'b--', label='Numerical')
    axs[2].set_ylabel("Velocity (m/s)")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_title("Velocity vs Time")
    axs[2].legend(); axs[2].grid(True)
    
    plt.tight_layout()
    plt.show()

def plot_transient_vs_steady(ana):
    t = ana['time']
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(t, ana['transient_x'], 'b--', label='Transient Component (Decaying)')
    ax.plot(t, ana['steady_state_x'], 'g-.', label='Steady-State Component (Periodic)')
    ax.plot(t, ana['displacement'], 'k-', lw=2, alpha=0.7, label='Total Response')
    
    ax.set_title("Superposition: Transient vs Steady-State Response")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Displacement (m)")
    ax.grid(True); ax.legend()
    plt.tight_layout()
    plt.show()

def plot_forced_phase_space(osc_base, forcing):
    # Run two different initial conditions
    osc1 = DampedOscillator(osc_base.m, osc_base.b, osc_base.k, 0, 0, duration=30, forcing_function=forcing)
    osc2 = DampedOscillator(osc_base.m, osc_base.b, osc_base.k, 1, 0, duration=30, forcing_function=forcing)
    
    res1, res2 = osc1.simulate(), osc2.simulate()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(res1['displacement'], res1['velocity'], 'b-', alpha=0.6, label='IC: (0, 0)')
    ax.plot(res2['displacement'], res2['velocity'], 'r-', alpha=0.6, label='IC: (1, 0)')
    
    # Highlight steady-state limit cycle (last 10% of time)
    steady_idx = int(len(res1['time']) * 0.9)
    ax.plot(res1['displacement'][steady_idx:], res1['velocity'][steady_idx:], 'k-', lw=2, label='Steady-State Limit Cycle')
    
    ax.set_title("Forced Phase-Space Trajectory\n(Trajectories converge to the same periodic orbit)")
    ax.set_xlabel("Displacement (m)")
    ax.set_ylabel("Velocity (m/s)")
    ax.axhline(0, color='black', lw=0.5); ax.axvline(0, color='black', lw=0.5)
    ax.grid(True); ax.legend()
    plt.tight_layout()
    plt.show()

def export_forced_csv(num, ana, en):
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'forced'), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'forced', 'forced_oscillator.csv')
    
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'F_drive', 'Num_Disp', 'Ana_Disp', 'Num_Vel', 'Ana_Vel', 'P_drive', 'P_damping', 'R_E'])
        for i in range(len(num['time'])):
            writer.writerow([
                num['time'][i], num['external_force'][i], 
                num['displacement'][i], ana['displacement'][i],
                num['velocity'][i], ana['velocity'][i],
                en['P_drive'][i], en['P_d'][i], en['R_E'][i]
            ])

if __name__ == "__main__":
    run_forced_experiment()
