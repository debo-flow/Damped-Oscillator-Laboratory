"""
Milestone 17: Intermittency Analysis
Detects laminar/burst phases and evaluates power-law scaling.
"""

import numpy as np
from typing import Dict, Tuple

class IntermittencyAnalyzer:
    @staticmethod
    def segment_phases(time_series: np.ndarray, window: int = 50, variance_threshold: float = 0.1) -> Dict:
        """Segments a trajectory into laminar (low variance) and burst (high variance) phases."""
        is_burst = np.zeros(len(time_series), dtype=bool)
        
        for i in range(len(time_series) - window):
            segment = time_series[i:i+window]
            if np.var(segment) > variance_threshold:
                is_burst[i:i+window] = True
                
        # Calculate lengths of laminar episodes
        laminar_lengths = []
        current_len = 0
        for b in is_burst:
            if not b:
                current_len += 1
            else:
                if current_len > 0:
                    laminar_lengths.append(current_len)
                    current_len = 0
        if current_len > 0:
            laminar_lengths.append(current_len)
            
        return {
            'burst_mask': is_burst,
            'laminar_lengths': np.array(laminar_lengths),
            'mean_laminar_length': np.mean(laminar_lengths) if laminar_lengths else 0.0
        }

    @staticmethod
    def fit_scaling_law(mu_vals: np.ndarray, mu_c: float, mean_lengths: np.ndarray) -> Dict:
        """Fits <L> ~ |mu - mu_c|^-gamma for intermittency."""
        diffs = np.abs(mu_vals - mu_c)
        valid = (diffs > 1e-5) & (mean_lengths > 0)
        
        if np.sum(valid) < 3:
            return {'gamma': np.nan, 'r_squared': 0.0}
            
        log_diffs = np.log(diffs[valid])
        log_L = np.log(mean_lengths[valid])
        
        slope, intercept = np.polyfit(log_diffs, log_L, 1)
        r_matrix = np.corrcoef(log_diffs, log_L)
        r_sq = r_matrix[0, 1]**2
        
        return {
            'gamma_estimate': -slope,
            'fit_quality_r2': r_sq,
            'is_power_law': r_sq > 0.90
        }
