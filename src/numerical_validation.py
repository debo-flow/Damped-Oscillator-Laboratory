"""
Milestone 19: Numerical Validation & Error Metrics
Validates trajectories against analytical solutions and physical conservation laws.
"""

import numpy as np
from typing import Dict

class NumericalValidator:
    @staticmethod
    def calculate_errors(y_num: np.ndarray, y_exact: np.ndarray) -> Dict[str, float]:
        """Calculates standard numerical error metrics."""
        diff = y_num - y_exact
        abs_err = np.abs(diff)
        
        # Safe relative error avoiding division by zero
        safe_denom = np.where(np.abs(y_exact) < 1e-12, 1e-12, np.abs(y_exact))
        rel_err = abs_err / safe_denom

        return {
            'max_abs_error': float(np.max(abs_err)),
            'rmse': float(np.sqrt(np.mean(diff**2))),
            'mae': float(np.mean(abs_err)),
            'max_rel_error': float(np.max(rel_err)),
            'final_state_error': float(np.linalg.norm(diff[:, -1]) if diff.ndim > 1 else np.abs(diff[-1]))
        }

    @staticmethod
    def validate_energy_balance(t: np.ndarray, x: np.ndarray, v: np.ndarray, 
                                m: float, k: float, c: float) -> Dict[str, np.ndarray]:
        """
        Validates energy balance: E(t) - E(0) = \int -c v^2 dt (for free damped oscillator).
        """
        E_kinetic = 0.5 * m * v**2
        E_potential = 0.5 * k * x**2
        E_total = E_kinetic + E_potential
        
        # Integrate dissipated power: P_diss = -c * v^2
        power_dissipated = -c * v**2
        from scipy.integrate import cumulative_trapezoid
        work_dissipated = cumulative_trapezoid(power_dissipated, t, initial=0.0)
        
        # Residual: E(t) should equal E(0) + Work Dissipated
        E_expected = E_total[0] + work_dissipated
        residual = E_total - E_expected
        
        return {
            'E_total': E_total,
            'work_dissipated': work_dissipated,
            'residual': residual,
            'max_residual': np.max(np.abs(residual))
        }
