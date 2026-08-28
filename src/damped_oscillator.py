"""
Milestone 6: Damped Oscillator Model
Simulates a damped harmonic oscillator with optional external forcing.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, Optional, Callable
from forcing import ForcingFunction, ZeroForcing

class DampedOscillator:
    def __init__(
        self, m: float = 1.0, b: float = 0.5, k: float = 10.0, 
        x0: float = 1.0, v0: float = 0.0, duration: float = 10.0, 
        num_samples: int = 1000, forcing_function: Optional[ForcingFunction] = None
    ):
        if m <= 0: raise ValueError("Mass (m) must be strictly greater than 0.")
        if k <= 0: raise ValueError("Spring constant (k) must be strictly greater than 0.")
        if b < 0: raise ValueError("Damping coefficient (b) must be non-negative.")
        if duration <= 0: raise ValueError("Simulation duration must be > 0.")
        if num_samples < 10: raise ValueError("Samples must be >= 10.")

        self.m = m
        self.b = b
        self.k = k
        self.x0 = x0
        self.v0 = v0
        self.duration = duration
        self.num_samples = num_samples
        self.forcing_function = forcing_function if forcing_function else ZeroForcing()

    @property
    def omega_0(self) -> float: return np.sqrt(self.k / self.m)

    @property
    def f_0(self) -> float: return self.omega_0 / (2 * np.pi)

    @property
    def zeta(self) -> float: return self.b / (2 * np.sqrt(self.m * self.k))

    @property
    def discriminant(self) -> float: return self.b**2 - 4 * self.m * self.k

    @property
    def regime(self) -> str:
        if np.isclose(self.zeta, 1.0, atol=1e-7): return "Critically Damped"
        elif self.zeta < 1.0: return "Underdamped"
        else: return "Overdamped"

    @property
    def omega_d(self) -> Optional[float]:
        if self.regime == "Underdamped": return self.omega_0 * np.sqrt(1 - self.zeta**2)
        return None

    def _ode_system(self, t: float, y: list) -> list:
        x, v = y
        F_ext = self.forcing_function(t)
        dxdt = v
        dvdt = (F_ext - self.b * v - self.k * x) / self.m
        return [dxdt, dvdt]

    def simulate(self, rtol: float = 1e-5, atol: float = 1e-8, max_step: float = np.inf) -> Dict[str, np.ndarray]:
        t_span = (0, self.duration)
        t_eval = np.linspace(0, self.duration, self.num_samples)
        y0 = [self.x0, self.v0]

        sol = solve_ivp(
            self._ode_system, t_span, y0, t_eval=t_eval, method='RK45',
            rtol=rtol, atol=atol, max_step=max_step
        )
        
        t, x, v = sol.t, sol.y[0], sol.y[1]
        
        return {
            'time': t, 'displacement': x, 'velocity': v,
            'kinetic_energy': 0.5 * self.m * v**2,
            'potential_energy': 0.5 * self.k * x**2,
            'total_energy': 0.5 * self.m * v**2 + 0.5 * self.k * x**2,
            'external_force': np.array([self.forcing_function(ti) for ti in t])
        }

