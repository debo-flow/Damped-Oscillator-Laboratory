"""
Milestone 17: Transient Chaos & Escape Dynamics
Tracks finite-time Lyapunov exponents and escape-time survival distributions.
"""

import numpy as np
from scipy.optimize import curve_fit
from typing import Dict, List

class TransientChaosAnalyzer:
    @staticmethod
    def detect_escape(trajectory: np.ndarray, boundary_threshold: float = 10.0) -> int:
        """Returns the index where the trajectory escapes a bounded region, or -1 if it remains bounded."""
        norms = np.linalg.norm(trajectory, axis=1)
        escape_indices = np.where(norms > boundary_threshold)[0]
        if len(escape_indices) > 0:
            return escape_indices[0]
        return -1

    @staticmethod
    def survival_function(escape_times: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates P(tau > t)."""
        sorted_times = np.sort(escape_times)
        p_survival = 1.0 - np.arange(1, len(sorted_times) + 1) / len(sorted_times)
        return sorted_times, p_survival

    @staticmethod
    def fit_exponential_escape(times: np.ndarray, p_survival: np.ndarray) -> Dict:
        """Fits P(tau > t) = exp(-kappa * t) to estimate the escape rate kappa."""
        valid = p_survival > 0
        t_valid = times[valid]
        log_p = np.log(p_survival[valid])
        
        if len(t_valid) < 3:
            return {'kappa': np.nan, 'r_squared': 0.0}
            
        slope, intercept = np.polyfit(t_valid, log_p, 1)
        r_matrix = np.corrcoef(t_valid, log_p)
        r_sq = r_matrix[0, 1]**2
        
        kappa = -slope
        return {
            'escape_rate_kappa': kappa,
            'fit_quality_r2': r_sq,
            'is_exponential': r_sq > 0.95
        }
        
    @staticmethod
    def windowed_lyapunov(times: np.ndarray, local_lyapunovs: np.ndarray, window_size: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates a moving average of the local Lyapunov exponent to detect internal regime shifts."""
        if len(local_lyapunovs) < window_size:
            return times, local_lyapunovs
            
        window = np.ones(window_size) / window_size
        smoothed_le = np.convolve(local_lyapunovs, window, mode='valid')
        smoothed_times = times[window_size//2 : len(smoothed_le) + window_size//2]
        return smoothed_times, smoothed_le
