"""
Milestone 18: Parameter Estimation & Identifiability
Recovers physical parameters from time-series data and quantifies uncertainty.
"""

import numpy as np
from scipy.optimize import least_squares
from typing import Callable, Dict, Tuple, List

class ParameterEstimator:
    def __init__(self, model_residual_func: Callable, param_names: List[str]):
        """
        model_residual_func: f(params, t, x_observed) -> residual_array
        """
        self.residual_func = model_residual_func
        self.param_names = param_names

    def estimate(self, t: np.ndarray, x_obs: np.ndarray, initial_guess: List[float], 
                 bounds: Tuple[List[float], List[float]] = (-np.inf, np.inf)) -> Dict:
        """Estimates parameters using nonlinear least squares."""
        
        # Optimize
        result = least_squares(self.residual_func, initial_guess, args=(t, x_obs), bounds=bounds)
        
        p_opt = result.x
        J = result.jac
        residuals = result.fun
        
        # Identifiability & Uncertainty (Fisher Information Matrix approximation)
        # H approx J^T J
        H = J.T @ J
        
        try:
            cov_matrix = np.linalg.inv(H) * (np.sum(residuals**2) / (len(residuals) - len(p_opt)))
            std_errors = np.sqrt(np.diag(cov_matrix))
            cond_number = np.linalg.cond(H)
        except np.linalg.LinAlgError:
            cov_matrix = np.full((len(p_opt), len(p_opt)), np.nan)
            std_errors = np.full(len(p_opt), np.nan)
            cond_number = np.inf

        # Diagnostics
        if cond_number > 1e8: identifiability = "poorly_identifiable"
        elif cond_number > 1e4: identifiability = "weakly_identifiable"
        else: identifiability = "identifiable_candidate"

        return {
            'estimated_parameters': {name: val for name, val in zip(self.param_names, p_opt)},
            'standard_errors': {name: err for name, err in zip(self.param_names, std_errors)},
            'condition_number': cond_number,
            'identifiability': identifiability,
            'success': result.success,
            'cost': result.cost
        }
