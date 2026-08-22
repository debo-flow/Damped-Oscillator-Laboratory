
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Dict, Optional


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
        # Parameter Validation
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

        self.m = m
        self.b = b
        self.k = k
        self.x0 = x0
        self.v0 = v0
        self.duration = duration
        self.num_samples = num_samples

    # --- Physical & Mathematical Properties ---

    @property
    def omega_0(self) -> float:
        """Natural angular frequency (rad/s)"""
        return np.sqrt(self.k / self.m)

    @property
    def f_0(self) -> float:
        """Natural frequency (Hz)"""
        return self.omega_0 / (2 * np.pi)

    @property
    def zeta(self) -> float:
        """Damping ratio"""
        return self.b / (2 * np.sqrt(self.m * self.k))

    @property
    def discriminant(self) -> float:
        """Discriminant of the characteristic equation (b^2 - 4mk)"""
        return self.b**2 - 4 * self.m * self.k

    @property
    def regime(self) -> str:
        """Classification of the damping regime"""
        if np.isclose(self.zeta, 1.0, atol=1e-7):
            return "Critically Damped"
        elif self.zeta < 1.0:
            return "Underdamped"
        else:
            return "Overdamped"

    @property
    def omega_d(self) -> Optional[float]:
        """Damped angular frequency (rad/s). Only applicable for underdamped systems."""
        if self.regime == "Underdamped":
            return self.omega_0 * np.sqrt(1 - self.zeta**2)
        return None

    # --- Numerical Simulation ---

    def _ode_system(self, t: float, y: list) -> list:
        x, v = y
        dxdt = v
        dvdt = -(self.b / self.m) * v - (self.k / self.m) * x
        return [dxdt, dvdt]

    def simulate(self) -> Dict[str, np.ndarray]:
        t_span = (0, self.duration)
        t_eval = np.linspace(0, self.duration, self.num_samples)
        y0 = [self.x0, self.v0]

        sol = solve_ivp(self._ode_system, t_span, y0, t_eval=t_eval, method='RK45')

        t, x, v = sol.t, sol.y[0], sol.y[1]
        kinetic_energy = 0.5 * self.m * v**2
        potential_energy = 0.5 * self.k * x**2

        return {
            'time': t,
            'displacement': x,
            'velocity': v,
            'kinetic_energy': kinetic_energy,
            'potential_energy': potential_energy,
            'total_energy': kinetic_energy + potential_energy
        }

    # --- Analytical Solution ---

    def analytical_solution(self, t: np.ndarray) -> np.ndarray:
        """Calculates the analytical displacement over an array of times."""
        if self.regime == "Underdamped":
            w_d = self.omega_d
            # Constants derivation from initial conditions
            a_cos_phi = self.x0
            a_sin_phi = -(self.v0 + self.zeta * self.omega_0 * self.x0) / w_d
            A = np.sqrt(a_cos_phi**2 + a_sin_phi**2)
            phi = np.arctan2(a_sin_phi, a_cos_phi)
            return A * np.exp(-self.zeta * self.omega_0 * t) * np.cos(w_d * t + phi)

        elif self.regime == "Critically Damped":
            A = self.x0
            B = self.v0 + self.omega_0 * self.x0
            return (A + B * t) * np.exp(-self.omega_0 * t)

        else: # Overdamped
            r1 = (-self.b + np.sqrt(self.discriminant)) / (2 * self.m)
            r2 = (-self.b - np.sqrt(self.discriminant)) / (2 * self.m)
            B = (self.v0 - self.x0 * r1) / (r2 - r1)
            A = self.x0 - B
            return A * np.exp(r1 * t) + B * np.exp(r2 * t)
