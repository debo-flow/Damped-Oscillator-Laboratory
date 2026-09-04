"""
Lyapunov Exponents, Kaplan-Yorke Dimension & Full Spectrum
Calculates LLE via Benettin, Full Spectrum via QR-decomposition, and D_KY.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Callable, Dict, List, Tuple, Optional

try:
    from nonlinear_oscillators import DuffingOscillator
    from forcing import SinusoidalForcing
except ImportError:
    print("Warning: Prior milestone modules not found. Some features may be limited.")

class LyapunovAnalyzer:
    def __init__(self, ode_func: Callable, dimension: int):
        self.ode_func = ode_func
        self.dimension = dimension

    def numerical_jacobian(self, t: float, y: np.ndarray, h: float = 1e-6) -> np.ndarray:
        """Approximates the Jacobian matrix J = df/dy using central finite differences."""
        J = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            y_plus = np.copy(y)
            y_minus = np.copy(y)
            y_plus[i] += h
            y_minus[i] -= h
            
            f_plus = np.array(self.ode_func(t, y_plus))
            f_minus = np.array(self.ode_func(t, y_minus))
            
            J[:, i] = (f_plus - f_minus) / (2 * h)
        return J

    def calculate_largest_lyapunov(self, y0: np.ndarray, t_start: float = 0.0, 
                                   t_max: float = 500.0, tau_r: float = 1.0, 
                                   delta0: float = 1e-8, transient_time: float = 100.0,
                                   method: str = 'RK45', rtol: float = 1e-8, atol: float = 1e-8) -> Dict:
        """Calculates the Largest Lyapunov Exponent using Benettin's renormalization method."""
        # [Preserved exactly from Milestone 13. Omitted for brevity in this block, 
        # but KEEP your existing Milestone 13 implementation of this function here.]
        pass 

    def _tangent_ode(self, t: float, Y: np.ndarray) -> np.ndarray:
        """ODE system including both the physical state and the tangent space matrix V."""
        n = self.dimension
        x = Y[:n]
        V = Y[n:].reshape((n, n))
        
        dxdt = np.array(self.ode_func(t, x))
        J = self.numerical_jacobian(t, x)
        dVdt = J @ V
        
        return np.concatenate((dxdt, dVdt.flatten()))

    def calculate_full_spectrum(self, y0: np.ndarray, t_start: float = 0.0, 
                                t_max: float = 500.0, tau_r: float = 1.0, 
                                transient_time: float = 100.0,
                                method: str = 'RK45', rtol: float = 1e-8, atol: float = 1e-8) -> Dict:
        """Calculates the full Lyapunov spectrum using tangent space integration and QR decomposition."""
        if transient_time > 0:
            sol_trans = solve_ivp(self.ode_func, (t_start, t_start + transient_time), y0, 
                                  method=method, rtol=rtol, atol=atol)
            if not sol_trans.success: raise RuntimeError("Transient integration failed.")
            y_curr = sol_trans.y[:, -1]
            t_curr = t_start + transient_time
        else:
            y_curr = np.array(y0, dtype=float)
            t_curr = t_start

        # Initialize orthogonal tangent space basis (Identity matrix)
        n = self.dimension
        V_curr = np.eye(n)
        
        num_steps = int((t_max - transient_time) / tau_r)
        
        times = []
        spectrum_history = []
        S_i = np.zeros(n)
        ortho_errors = []
        
        for step in range(1, num_steps + 1):
            t_next = t_curr + tau_r
            Y_init = np.concatenate((y_curr, V_curr.flatten()))
            
            sol = solve_ivp(self._tangent_ode, (t_curr, t_next), Y_init, 
                            method=method, rtol=rtol, atol=atol)
            if not sol.success:
                return {'converged': False, 'error': 'Tangent integration diverged.'}
                
            Y_final = sol.y[:, -1]
            y_curr = Y_final[:n]
            V_final = Y_final[n:].reshape((n, n))
            
            # QR Reorthonormalization
            Q, R = np.linalg.qr(V_final)
            
            # Diagnostic: Orthogonality error |Q^T Q - I|
            E_Q = np.linalg.norm(Q.T @ Q - np.eye(n))
            ortho_errors.append(E_Q)
            
            # Enforce positive diagonals on R for consistent log calculation
            signs = np.sign(np.diag(R))
            signs[signs == 0] = 1
            R_pos = R * signs[:, np.newaxis]
            Q_pos = Q * signs
            
            S_i += np.log(np.diag(R_pos))
            V_curr = Q_pos
            t_curr = t_next
            
            times.append(t_curr)
            spectrum_history.append(S_i / (step * tau_r))

        spectrum_history = np.array(spectrum_history)
        final_spectrum = np.sort(spectrum_history[-1])[::-1] # Order descending
        
        # Divergence comparison (Sum of Exponents)
        sum_lyapunov = np.sum(final_spectrum)
        
        return {
            'times': np.array(times),
            'spectrum_history': spectrum_history,
            'final_spectrum': final_spectrum,
            'sum_lyapunov': sum_lyapunov,
            'orthogonality_errors': np.array(ortho_errors),
            'kaplan_yorke_dim': self.kaplan_yorke_dimension(final_spectrum),
            'positive_lyapunov_sum': np.sum(final_spectrum[final_spectrum > 0]),
            'converged': True
        }

    @staticmethod
    def kaplan_yorke_dimension(spectrum: np.ndarray) -> float:
        """Calculates D_KY = j + sum(L_1..L_j) / |L_{j+1}|."""
        spectrum = np.sort(spectrum)[::-1]
        cumulative_sum = np.cumsum(spectrum)
        
        if cumulative_sum[0] < 0:
            return 0.0 # Purely dissipative sink
        if cumulative_sum[-1] > 0:
            return float(len(spectrum)) # Completely divergent source
            
        # Find j where sum is positive, but adding j+1 makes it negative
        j = np.where(cumulative_sum >= 0)[0][-1]
        
        if j + 1 < len(spectrum):
            D_KY = (j + 1) + (cumulative_sum[j] / abs(spectrum[j+1]))
            return D_KY
        return float(len(spectrum))

