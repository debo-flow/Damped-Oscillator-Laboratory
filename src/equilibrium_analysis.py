"""
Equilibrium Analysis & Stability Tracking
Finds equilibria, tracks eigenvalues, and detects Saddle-Node/Hopf candidates.
"""

import numpy as np
from scipy.optimize import fsolve
from typing import Callable, Dict, List, Tuple

class EquilibriumAnalyzer:
    def __init__(self, ode_func: Callable, dimension: int):
        self.ode_func = ode_func
        self.dimension = dimension

    def _steady_state_residual(self, x: np.ndarray, params: Dict) -> np.ndarray:
        """Returns the derivative dx/dt evaluated at t=0 (autonomous assumption)."""
        return np.array(self.ode_func(0.0, x, params))

    def find_equilibrium(self, guess: np.ndarray, params: Dict, tol: float = 1e-9) -> Dict:
        """Finds equilibrium points using numerical root finding."""
        x_eq, info, ier, msg = fsolve(self._steady_state_residual, guess, args=(params,), 
                                      xtol=tol, full_output=True)
        residual = np.linalg.norm(self._steady_state_residual(x_eq, params))
        
        return {
            'equilibrium_state': x_eq,
            'residual_norm': residual,
            'converged': (ier == 1) and (residual < 1e-6),
            'solver_msg': msg
        }

    def numerical_jacobian(self, x: np.ndarray, params: Dict, h: float = 1e-6) -> np.ndarray:
        """Central finite difference Jacobian at an equilibrium point."""
        J = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            x_plus, x_minus = np.copy(x), np.copy(x)
            x_plus[i] += h
            x_minus[i] -= h
            f_plus = self._steady_state_residual(x_plus, params)
            f_minus = self._steady_state_residual(x_minus, params)
            J[:, i] = (f_plus - f_minus) / (2 * h)
        return J

    def analyze_stability(self, x_eq: np.ndarray, params: Dict) -> Dict:
        """Calculates eigenvalues and classifies stability."""
        J = self.numerical_jacobian(x_eq, params)
        eigenvalues = np.linalg.eigvals(J)
        max_real = np.max(np.real(eigenvalues))
        
        if max_real < -1e-5:
            stability = "stable"
        elif max_real > 1e-5:
            stability = "unstable"
        else:
            stability = "marginal"
            
        # Candidate Detection
        saddle_node_candidate = any(abs(np.real(e)) < 1e-3 and abs(np.imag(e)) < 1e-3 for e in eigenvalues)
        hopf_candidate = any(abs(np.real(e)) < 1e-3 and abs(np.imag(e)) > 1e-3 for e in eigenvalues)
        
        event = "none"
        if saddle_node_candidate: event = "saddle_node_candidate"
        if hopf_candidate: event = "hopf_candidate"
        
        return {
            'eigenvalues': eigenvalues,
            'max_real_part': max_real,
            'stability': stability,
            'event': event
        }
