
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Dict, Any


class DampedOscillator:
    """
    Physics engine for a 1D damped harmonic oscillator.
    Equation of motion: m*x'' + b*x' + k*x = 0
    """
    def __init__(
        self,
        m: float = 1.0,
        b: float = 0.5,
        k: float = 10.0,
        x0: float = 1.0,
        v0: float = 0.0,
        duration: float = 10.0,
        num_samples: int = 1000
    ):
        # 1. Parameter Validation
        if m <= 0:
            raise ValueError("Mass (m) must be strictly greater than 0.")
        if k <= 0:
            raise ValueError("Spring constant (k) must be strictly greater than 0.")
        if b < 0:
            raise ValueError("Damping coefficient (b) must be non-negative.")
        if duration <= 0:
            raise ValueError("Simulation duration must be greater than 0.")
        if num_samples < 10:
            raise ValueError("Number of time samples must be sufficiently large (>=10).")

        # 2. Assignment
        self.m = m
        self.b = b
        self.k = k
        self.x0 = x0
        self.v0 = v0
        self.duration = duration
        self.num_samples = num_samples

    def _ode_system(self, t: float, y: list) -> list:
        """
        Converts the second-order ODE into a system of two first-order ODEs.
        y[0] = x (displacement)
        y[1] = v (velocity)
        """
        x, v = y
        dxdt = v
        dvdt = -(self.b / self.m) * v - (self.k / self.m) * x
        return [dxdt, dvdt]

    def simulate(self) -> Dict[str, np.ndarray]:
        """
        Runs the numerical integration and calculates physical quantities.
        Returns a dictionary containing time, displacement, velocity, and energies.
        """
        t_span = (0, self.duration)
        t_eval = np.linspace(0, self.duration, self.num_samples)
        y0 = [self.x0, self.v0]

        # Solve the IVP
        sol = solve_ivp(self._ode_system, t_span, y0, t_eval=t_eval, method='RK45')

        t = sol.t
        x = sol.y[0]
        v = sol.y[1]

        # Calculate Energies
        kinetic_energy = 0.5 * self.m * v**2
        potential_energy = 0.5 * self.k * x**2
        total_energy = kinetic_energy + potential_energy

        return {
            'time': t,
            'displacement': x,
            'velocity': v,
            'kinetic_energy': kinetic_energy,
            'potential_energy': potential_energy,
            'total_energy': total_energy
        }


def plot_results(results: Dict[str, np.ndarray]):
    """
    Generates three separate Matplotlib figures for the simulation results.
    """
    t = results['time']
    x = results['displacement']
    v = results['velocity']
    k_e = results['kinetic_energy']
    p_e = results['potential_energy']
    e_tot = results['total_energy']

    # Figure 1: Displacement vs Time
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(t, x, color='blue', label='Displacement $x(t)$')
    ax1.set_title("Damped Oscillator: Displacement vs Time")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Displacement (m)")
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    fig1.tight_layout()

    # Figure 2: Velocity vs Time
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(t, v, color='red', label='Velocity $v(t)$')
    ax2.set_title("Damped Oscillator: Velocity vs Time")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity (m/s)")
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    fig2.tight_layout()

    # Figure 3: Energy vs Time
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    ax3.plot(t, k_e, color='green', label='Kinetic Energy ($K$)', alpha=0.8)
    ax3.plot(t, p_e, color='orange', label='Potential Energy ($U$)', alpha=0.8)
    ax3.plot(t, e_tot, color='black', label='Total Energy ($E$)', linewidth=2)
    ax3.set_title("Damped Oscillator: Mechanical Energy vs Time")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Energy (Joules)")
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.legend()
    fig3.tight_layout()

    # Render plots
    plt.show()


if __name__ == "__main__":
    # Execute simulation with default parameters for Milestone 1 validation
    try:
        print("Initializing Damped Oscillator...")
        oscillator = DampedOscillator(
            m=1.0, 
            b=0.5, 
            k=10.0, 
            x0=1.0, 
            v0=0.0, 
            duration=15.0, 
            num_samples=1500
        )
        
        print("Running simulation...")
        sim_results = oscillator.simulate()
        
        print("Simulation complete. Generating plots...")
        plot_results(sim_results)
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
