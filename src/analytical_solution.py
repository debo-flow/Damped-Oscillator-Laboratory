"""
Milestone 3: Analytical Solution Engine
Calculates exact mathematical displacement and velocity for damped oscillators.
"""

import numpy as np
from typing import Dict

class AnalyticalSolver:
    def __init__(self, m: float, b: float, k: float, x0: float, v0: float):
        self.m = m
        self.b = b
        self.k = k
        self.x0 = x0
        self.v0 = v0
        self.w0 = np.sqrt(k / m)
        self.zeta = b / (2 * np.sqrt(m * k))

    def solve(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        if np.isclose(self.zeta, 1.0, atol=1e-7):
            return self._critically_damped(t)
        elif self.zeta < 1.0:
            return self._underdamped(t)
        else:
            return self._overdamped(t)

    def _underdamped(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        wd = self.w0 * np.sqrt(1 - self.zeta**2)
        A = self.x0
        B = (self.v0 + self.zeta * self.w0 * self.x0) / wd
        
        decay = np.exp(-self.zeta * self.w0 * t)
        cos_wt = np.cos(wd * t)
        sin_wt = np.sin(wd * t)
        
        x = decay * (A * cos_wt + B * sin_wt)
        v = decay * ((B * wd - A * self.zeta * self.w0) * cos_wt - (A * wd + B * self.zeta * self.w0) * sin_wt)
        
        return {'time': t, 'displacement': x, 'velocity': v}

    def _critically_damped(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        A = self.x0
        B = self.v0 + self.w0 * self.x0
        
        decay = np.exp(-self.w0 * t)
        x = (A + B * t) * decay
        v = (B - self.w0 * (A + B * t)) * decay
        
        return {'time': t, 'displacement': x, 'velocity': v}

    def _overdamped(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        disc = np.sqrt(self.b**2 - 4 * self.m * self.k)
        r1 = (-self.b + disc) / (2 * self.m)
        r2 = (-self.b - disc) / (2 * self.m)
        
        B = (self.v0 - r1 * self.x0) / (r2 - r1)
        A = self.x0 - B
        
        x = A * np.exp(r1 * t) + B * np.exp(r2 * t)
        v = A * r1 * np.exp(r1 * t) + B * r2 * np.exp(r2 * t)
        
        return {'time': t, 'displacement': x, 'velocity': v}
