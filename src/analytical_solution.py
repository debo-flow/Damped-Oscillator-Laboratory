"""
Milestone 6: Analytical Solution Engine
Calculates exact mathematical responses, now supporting forced oscillators.
"""

import numpy as np
from typing import Dict, Optional

class AnalyticalSolver:
    def __init__(self, m: float, b: float, k: float, x0: float, v0: float, 
                 F0: float = 0.0, omega_f: float = 0.0):
        self.m, self.b, self.k = m, b, k
        self.x0, self.v0 = x0, v0
        self.F0, self.omega_f = F0, omega_f
        self.w0 = np.sqrt(k / m)
        self.zeta = b / (2 * np.sqrt(m * k))

    def _steady_state(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        if self.F0 == 0.0:
            return {'x': np.zeros_like(t), 'v': np.zeros_like(t)}
            
        # Amplitude and Phase
        denominator = np.sqrt((self.k - self.m * self.omega_f**2)**2 + (self.b * self.omega_f)**2)
        X = self.F0 / denominator
        phi = np.arctan2(self.b * self.omega_f, self.k - self.m * self.omega_f**2)
        
        x_ss = X * np.cos(self.omega_f * t - phi)
        v_ss = -X * self.omega_f * np.sin(self.omega_f * t - phi)
        return {'x': x_ss, 'v': v_ss, 'X_amp': X, 'phi': phi}

    def _transient_ics(self) -> tuple:
        """Finds effective initial conditions for the transient component."""
        ss_0 = self._steady_state(np.array([0.0]))
        x0_trans = self.x0 - ss_0['x'][0]
        v0_trans = self.v0 - ss_0['v'][0]
        return x0_trans, v0_trans

    def solve(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        # 1. Steady State Response
        ss = self._steady_state(t)
        
        # 2. Transient Response (using effective ICs)
        x0_t, v0_t = self._transient_ics()
        
        if np.isclose(self.zeta, 1.0, atol=1e-7): trans = self._critically_damped(t, x0_t, v0_t)
        elif self.zeta < 1.0: trans = self._underdamped(t, x0_t, v0_t)
        else: trans = self._overdamped(t, x0_t, v0_t)
            
        # 3. Superposition
        return {
            'time': t,
            'displacement': trans['x'] + ss['x'],
            'velocity': trans['v'] + ss['v'],
            'transient_x': trans['x'],
            'steady_state_x': ss['x'],
            'amplitude': ss.get('X_amp', 0.0),
            'phase': ss.get('phi', 0.0)
        }

    def _underdamped(self, t: np.ndarray, x0: float, v0: float) -> Dict[str, np.ndarray]:
        wd = self.w0 * np.sqrt(1 - self.zeta**2)
        A = x0
        B = (v0 + self.zeta * self.w0 * x0) / wd
        decay = np.exp(-self.zeta * self.w0 * t)
        
        x = decay * (A * np.cos(wd * t) + B * np.sin(wd * t))
        v = decay * ((B * wd - A * self.zeta * self.w0) * np.cos(wd * t) - 
                     (A * wd + B * self.zeta * self.w0) * np.sin(wd * t))
        return {'x': x, 'v': v}

    def _critically_damped(self, t: np.ndarray, x0: float, v0: float) -> Dict[str, np.ndarray]:
        A = x0
        B = v0 + self.w0 * x0
        decay = np.exp(-self.w0 * t)
        
        x = (A + B * t) * decay
        v = (B - self.w0 * (A + B * t)) * decay
        return {'x': x, 'v': v}

    def _overdamped(self, t: np.ndarray, x0: float, v0: float) -> Dict[str, np.ndarray]:
        disc = np.sqrt(self.b**2 - 4 * self.m * self.k)
        r1 = (-self.b + disc) / (2 * self.m)
        r2 = (-self.b - disc) / (2 * self.m)
        
        B = (v0 - r1 * x0) / (r2 - r1)
        A = x0 - B
        
        x = A * np.exp(r1 * t) + B * np.exp(r2 * t)
        v = A * r1 * np.exp(r1 * t) + B * r2 * np.exp(r2 * t)
        return {'x': x, 'v': v}
