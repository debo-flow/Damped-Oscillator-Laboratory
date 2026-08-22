"""
Milestone 2: Damping Regimes Analysis
Simulates, compares, and evaluates numerical vs analytical solutions 
across the three fundamental damping regimes.
"""

import numpy as np
import matplotlib.pyplot as plt
from damped_oscillator import DampedOscillator

def run_analysis():
    # Common parameters
    m, k = 1.0, 10.0
    x0, v0 = 1.0, 0.0
    duration, num_samples = 10.0, 1000

    # Damping configurations
    configs = {
        "Underdamped": 0.5,
        "Critically Damped": 2 * np.sqrt(m * k), # 2 * sqrt(10)
        "Overdamped": 10.0
    }

    results = {}
    
    print("--- Damping Regimes Analysis ---")
    for name, b in configs.items():
        oscillator = DampedOscillator(m, b, k, x0, v0, duration, num_samples)
        sim = oscillator.simulate()
        
        t = sim['time']
        x_num = sim['displacement']
        x_ana = oscillator.analytical_solution(t)
        
        # Error calculation
        abs_err = np.abs(x_num - x_ana)
        max_err = np.max(abs_err)
        rms_err = np.sqrt(np.mean(abs_err**2))
        
        results[name] = {
            'time': t,
            'sim': sim,
            'x_ana': x_ana,
            'zeta': oscillator.zeta
        }
        
        print(f"[{name}] (zeta = {oscillator.zeta:.3f}, Delta = {oscillator.discriminant:.2f})")
        if oscillator.omega_d:
            print(f"  -> Damped Freq: {oscillator.omega_d:.3f} rad/s")
        print(f"  -> Max Abs Error: {max_err:.3e}")
        print(f"  -> RMS Error:     {rms_err:.3e}\n")

    plot_comparisons(results)


def plot_comparisons(results: dict):
    colors = {"Underdamped": "blue", "Critically Damped": "red", "Overdamped": "green"}

    # 1. Displacement Comparison
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    for name, res in results.items():
        ax1.plot(res['time'], res['sim']['displacement'], label=name, color=colors[name])
    ax1.set_title("Displacement vs Time: Damping Regimes")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Displacement (m)")
    ax1.axhline(0, color='black', linewidth=1, alpha=0.5)
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    fig1.tight_layout()

    # 2. Velocity Comparison
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    for name, res in results.items():
        ax2.plot(res['time'], res['sim']['velocity'], label=name, color=colors[name])
    ax2.set_title("Velocity vs Time: Damping Regimes")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity (m/s)")
    ax2.axhline(0, color='black', linewidth=1, alpha=0.5)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    fig2.tight_layout()

    # 3. Total Energy Comparison
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    for name, res in results.items():
        ax3.plot(res['time'], res['sim']['total_energy'], label=name, color=colors[name])
    ax3.set_title("Total Mechanical Energy Decay")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Total Energy (J)")
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.7)
    fig3.tight_layout()

    # 4. Numerical vs Analytical Subplots
    fig4, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (name, res) in zip(axes, results.items()):
        ax.plot(res['time'], res['sim']['displacement'], label='Numerical', lw=3, color='orange', alpha=0.7)
        ax.plot(res['time'], res['x_ana'], label='Analytical', lw=1.5, color='black', linestyle='--')
        ax.set_title(name)
        ax.set_xlabel("Time (s)")
        ax.grid(True, linestyle='--', alpha=0.7)
        if ax == axes[0]:
            ax.set_ylabel("Displacement (m)")
            ax.legend()
    fig4.tight_layout()

    # 5. Damping Ratio Classification Map
    fig5, ax5 = plt.subplots(figsize=(8, 2))
    ax5.plot([-0.2, 2.5], [0, 0], color='black', lw=1)
    
    for name, res in results.items():
        z = res['zeta']
        ax5.scatter([z], [0], color=colors[name], s=150, zorder=5)
        ax5.text(z, 0.15, f"{name}\n($\\zeta={z:.2f}$)", ha='center', va='bottom', color=colors[name], fontweight='bold')
    
    ax5.axvline(1.0, color='red', linestyle='--', alpha=0.3)
    ax5.set_xlim(-0.2, 2.5)
    ax5.set_ylim(-0.2, 0.6)
    ax5.set_yticks([])
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    ax5.spines['left'].set_visible(False)
    ax5.spines['bottom'].set_position('center')
    ax5.set_xlabel("Damping Ratio ($\\zeta$)")
    ax5.set_title("Damping Regime Classification")
    fig5.tight_layout()

    plt.show()

if __name__ == "__main__":
    run_analysis()
