"""
Milestone 4: Phase-Space Analysis Laboratory
Analyzes and visualizes the state-space dynamics of damped harmonic oscillators.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List
from damped_oscillator import DampedOscillator
from analytical_solution import AnalyticalSolver

class PhaseSpaceAnalyzer:
    def __init__(self, m: float, b: float, k: float):
        self.m = m
        self.b = b
        self.k = k
        self.w0 = np.sqrt(k / m)

    def get_equilibrium(self) -> Tuple[float, float]:
        """Identifies the (x, v) equilibrium point for the unforced oscillator."""
        return (0.0, 0.0)

    def state_derivative(self, x: float, v: float) -> Tuple[float, float]:
        """Calculates the state-space derivative: (x_dot, v_dot)."""
        x_dot = v
        v_dot = -(self.b / self.m) * v - (self.k / self.m) * x
        return x_dot, v_dot

    def calculate_phase_error(self, x_n: np.ndarray, v_n: np.ndarray, x_a: np.ndarray, v_a: np.ndarray) -> Dict[str, float]:
        """Calculates phase-space error vector metrics between numerical and analytical solutions."""
        e_phase = np.sqrt((x_n - x_a)**2 + (v_n - v_a)**2)
        return {
            'max_error': np.max(e_phase),
            'rms_error': np.sqrt(np.mean(e_phase**2)),
            'e_phase_series': e_phase
        }

    def calculate_metrics(self, t: np.ndarray, x: np.ndarray, v: np.ndarray, threshold: float = 1e-3) -> Dict[str, float]:
        """Calculates useful trajectory metrics like radii and threshold times."""
        radius = np.sqrt(x**2 + v**2)
        
        # Find first time the radius drops below threshold
        below_thresh_idx = np.where(radius < threshold)[0]
        t_thresh = t[below_thresh_idx[0]] if len(below_thresh_idx) > 0 else np.inf

        return {
            'initial_radius': radius[0],
            'final_radius': radius[-1],
            'max_x': np.max(np.abs(x)),
            'max_v': np.max(np.abs(v)),
            'time_to_threshold': t_thresh
        }

    def generate_vector_field(self, x_lim: Tuple[float, float], v_lim: Tuple[float, float], grid_size: int = 20):
        """Generates the meshgrid and derivatives for a phase-space vector field."""
        X, V = np.meshgrid(
            np.linspace(x_lim[0], x_lim[1], grid_size),
            np.linspace(v_lim[0], v_lim[1], grid_size)
        )
        U = V
        W = -(self.b / self.m) * V - (self.k / self.m) * X
        return X, V, U, W

    def generate_energy_contours(self, x_lim: Tuple[float, float], v_lim: Tuple[float, float], grid_size: int = 100):
        """Generates energy level grids for the undamped system to act as contours."""
        X, V = np.meshgrid(
            np.linspace(x_lim[0], x_lim[1], grid_size),
            np.linspace(v_lim[0], v_lim[1], grid_size)
        )
        E = 0.5 * self.m * V**2 + 0.5 * self.k * X**2
        return X, V, E


def plot_comprehensive_phase_portrait(m=1.0, b=0.5, k=10.0, dimensionless=False):
    """Plots a highly detailed phase portrait with time-coloring, vector fields, and energy contours."""
    analyzer = PhaseSpaceAnalyzer(m, b, k)
    osc = DampedOscillator(m, b, k, x0=1.0, v0=0.0, duration=15.0, num_samples=1500)
    res = osc.simulate()
    
    t, x, v = res['time'], res['displacement'], res['velocity']
    
    # Dimensionless normalization
    x_scale = 1.0 if not dimensionless else np.max(np.abs(x))
    v_scale = 1.0 if not dimensionless else x_scale * analyzer.w0
    
    x_plot, v_plot = x / x_scale, v / v_scale
    x_lim = (np.min(x_plot)*1.2, np.max(x_plot)*1.2)
    v_lim = (np.min(v_plot)*1.2, np.max(v_plot)*1.2)

    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 1. Energy Contours
    X, V, E = analyzer.generate_energy_contours(x_lim, v_lim)
    contour = ax.contour(X, V, E, levels=6, colors='gray', alpha=0.3, linestyles='dashed')
    ax.clabel(contour, inline=True, fontsize=8)

    # 2. Vector Field
    X_vf, V_vf, U_vf, W_vf = analyzer.generate_vector_field(x_lim, v_lim)
    ax.streamplot(X_vf, V_vf, U_vf, W_vf, color='lightgray', density=0.8, linewidth=0.8)

    # 3. Time-Colored Trajectory
    scatter = ax.scatter(x_plot, v_plot, c=t, cmap='viridis', s=2, zorder=5, label='Trajectory')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Time (s)')

    # 4. Equilibrium Point
    eq_x, eq_v = analyzer.get_equilibrium()
    ax.plot(eq_x, eq_v, 'r*', markersize=15, label='Equilibrium (0,0)', zorder=10)

    # Styling
    ax.set_title(f"Phase Portrait ({'Dimensionless' if dimensionless else 'Standard'}) - {osc.regime}")
    ax.set_xlabel("Displacement ($x/x_0$)" if dimensionless else "Displacement ($x$)")
    ax.set_ylabel("Velocity ($v/(x_0 \omega_0)$)" if dimensionless else "Velocity ($v$)")
    ax.axhline(0, color='black', lw=1, alpha=0.5)
    ax.axvline(0, color='black', lw=1, alpha=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


def plot_regime_comparison():
    """Plots all three fundamental damping regimes side-by-side in phase space."""
    configs = {
        "Underdamped": 0.5,
        "Critically Damped": 2 * np.sqrt(10.0), 
        "Overdamped": 10.0
    }
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Phase-Space Regime Comparison", fontsize=16)

    for ax, (name, b) in zip(axes, configs.items()):
        osc = DampedOscillator(m=1.0, b=b, k=10.0, x0=1.0, v0=0.0, duration=10.0, num_samples=1000)
        ana = AnalyticalSolver(m=1.0, b=b, k=10.0, x0=1.0, v0=0.0)
        
        num_res = osc.simulate()
        ana_res = ana.solve(num_res['time'])
        
        # Plot Both numerical and analytical
        ax.plot(ana_res['displacement'], ana_res['velocity'], 'k-', lw=3, alpha=0.5, label='Analytical')
        ax.plot(num_res['displacement'], num_res['velocity'], 'r--', lw=1.5, label='Numerical')
        
        ax.plot(0, 0, 'b*', markersize=12, label='Equilibrium')
        
        ax.set_title(name)
        ax.set_xlabel("Displacement $x$")
        ax.set_ylabel("Velocity $v$")
        ax.axhline(0, color='black', lw=0.5)
        ax.axvline(0, color='black', lw=0.5)
        ax.grid(True, linestyle='--', alpha=0.6)
        if ax == axes[0]:
            ax.legend()

    plt.tight_layout()
    plt.show()


def plot_multiple_initial_conditions():
    """Demonstrates how different starting states converge to the same equilibrium."""
    analyzer = PhaseSpaceAnalyzer(m=1.0, b=0.5, k=10.0) # Underdamped
    ics = [(1.0, 0.0), (0.5, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.5, -0.5)]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for x0, v0 in ics:
        osc = DampedOscillator(m=1.0, b=0.5, k=10.0, x0=x0, v0=v0, duration=15.0)
        res = osc.simulate()
        ax.plot(res['displacement'], res['velocity'], label=f"IC: x0={x0}, v0={v0}")
        ax.scatter([x0], [v0], color='black', s=20, zorder=5) # Mark start point
        
    eq_x, eq_v = analyzer.get_equilibrium()
    ax.plot(eq_x, eq_v, 'r*', markersize=15, label='Equilibrium (0,0)', zorder=10)

    ax.set_title("Phase Trajectories from Multiple Initial Conditions (Underdamped)")
    ax.set_xlabel("Displacement $x$")
    ax.set_ylabel("Velocity $v$")
    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Generating comprehensive phase portrait (Underdamped)...")
    plot_comprehensive_phase_portrait(m=1.0, b=0.5, k=10.0, dimensionless=True)
    
    print("Generating regime comparison...")
    plot_regime_comparison()
    
    print("Generating multiple initial conditions visualization...")
    plot_multiple_initial_conditions()

