"""
Periodic Orbit Analysis & Floquet Multipliers
Calculates Monodromy matrices, Floquet multipliers, and detects Period-Doubling/Torus bifurcations.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Dict

class PeriodicOrbitAnalyzer:
    def __init__(self, ode_func: Callable, jacobian_func: Callable, dimension: int, T_drive: float):
        self.ode_func = ode_func
        self.jacobian_func = jacobian_func
        self.dimension = dimension
        self.T_drive = T_drive

    def _monodromy_ode(self, t: float, Y: np.ndarray, params: Dict) -> np.ndarray:
        n = self.dimension
        x = Y[:n]
        Phi = Y[n:].reshape((n, n))
        
        dxdt = np.array(self.ode_func(t, x, params))
        J = self.jacobian_func(t, x, params)
        dPhidt = J @ Phi
        
        return np.concatenate((dxdt, dPhidt.flatten()))

    def calculate_floquet_multipliers(self, x0_poincare: np.ndarray, params: Dict) -> Dict:
        """Integrates over one period to get the Monodromy matrix and Floquet Multipliers."""
        n = self.dimension
        Phi_0 = np.eye(n)
        Y_0 = np.concatenate((x0_poincare, Phi_0.flatten()))
        
        sol = solve_ivp(self._monodromy_ode, (0, self.T_drive), Y_0, args=(params,),
                        method='RK45', rtol=1e-8, atol=1e-8)
        
        if not sol.success:
            return {'converged': False, 'error': 'Monodromy integration failed.'}
            
        Y_final = sol.y[:, -1]
        Monodromy = Y_final[n:].reshape((n, n))
        multipliers = np.linalg.eigvals(Monodromy)
        max_mag = np.max(np.abs(multipliers))
        
        if max_mag < 0.999: stability = "stable"
        elif max_mag > 1.001: stability = "unstable"
        else: stability = "marginal"
        
        # Candidate Detection
        pd_candidate = any(abs(np.real(m) + 1.0) < 1e-2 and abs(np.imag(m)) < 1e-2 for m in multipliers)
        torus_candidate = any(abs(np.abs(m) - 1.0) < 1e-2 and abs(np.imag(m)) > 1e-2 for m in multipliers)
        
        event = "none"
        if pd_candidate: event = "period_doubling_candidate"
        elif torus_candidate: event = "torus_candidate"
        
        return {
            'converged': True,
            'multipliers': multipliers,
            'max_magnitude': max_mag,
            'stability': stability,
            'event': event
        }
