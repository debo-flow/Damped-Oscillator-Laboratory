"""
Advanced Attractor Geometry Laboratory
Calculates Correlation Dimension, Box-Counting Dimension, and Phase-Space metrics.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from typing import Dict, Tuple

class AttractorAnalyzer:
    def __init__(self, trajectory: np.ndarray):
        """trajectory should be a shape (N, dim) array of post-transient states."""
        self.traj = trajectory
        self.N, self.dim = self.traj.shape

    def bounding_geometry(self) -> Dict:
        """Calculates bounding box, range, and centroid."""
        min_state = np.min(self.traj, axis=0)
        max_state = np.max(self.traj, axis=0)
        centroid = np.mean(self.traj, axis=0)
        rms_distance = np.sqrt(np.mean(np.sum((self.traj - centroid)**2, axis=1)))
        
        return {
            'min_state': min_state,
            'max_state': max_state,
            'range_state': max_state - min_state,
            'centroid': centroid,
            'rms_distance': rms_distance
        }

    def box_counting_dimension(self, epsilon_scales: np.ndarray = None) -> Dict:
        """Estimates fractal dimension using grid box counting."""
        if epsilon_scales is None:
            # Generate logarithmic scales relative to the attractor range
            geom = self.bounding_geometry()
            max_range = np.max(geom['range_state'])
            epsilon_scales = np.logspace(np.log10(max_range/100), np.log10(max_range/2), 15)

        counts = []
        valid_epsilons = []
        
        for eps in epsilon_scales:
            # Discretize states into grid boxes
            boxes = np.floor(self.traj / eps).astype(int)
            # Count unique boxes
            unique_boxes = np.unique(boxes, axis=0)
            counts.append(len(unique_boxes))
            valid_epsilons.append(eps)
            
        log_eps = np.log(1.0 / np.array(valid_epsilons))
        log_N = np.log(counts)
        
        # Fit scaling region using linear regression
        slope, intercept = np.polyfit(log_eps, log_N, 1)
        r_matrix = np.corrcoef(log_eps, log_N)
        r_squared = r_matrix[0, 1]**2
        
        # Guardrail: Do not fabricate a dimension if scaling is poor
        D_box = slope if r_squared > 0.95 else np.nan
        
        return {
            'epsilons': valid_epsilons, 'counts': counts,
            'log_1_over_eps': log_eps, 'log_N': log_N,
            'D_box': D_box, 'r_squared': r_squared
        }

    def correlation_dimension(self, r_scales: np.ndarray = None, max_points: int = 2000) -> Dict:
        """Estimates D2 using pairwise Grassberger-Procaccia correlation sums."""
        # Guardrail: Memory safeguard. Downsample if N is too large for O(N^2) pdist
        if self.N > max_points:
            step = self.N // max_points
            data = self.traj[::step]
            actual_n = len(data)
        else:
            data = self.traj
            actual_n = self.N
            
        distances = pdist(data)
        
        if r_scales is None:
            r_scales = np.logspace(np.log10(np.min(distances[distances>0])), np.log10(np.max(distances)/2), 20)
            
        c_sums = []
        for r in r_scales:
            c_sum = np.sum(distances < r) / (actual_n * (actual_n - 1) / 2.0)
            c_sums.append(c_sum)
            
        # Filter zero correlation sums for valid log calculation
        r_valid = np.array(r_scales)[np.array(c_sums) > 0]
        c_valid = np.array(c_sums)[np.array(c_sums) > 0]
        
        log_r = np.log(r_valid)
        log_C = np.log(c_valid)
        
        # Avoid saturated tails (r too small/large). Take the middle 60% of the log-log data
        if len(log_r) > 5:
            start, end = int(len(log_r)*0.2), int(len(log_r)*0.8)
            slope, intercept = np.polyfit(log_r[start:end], log_C[start:end], 1)
            r_matrix = np.corrcoef(log_r[start:end], log_C[start:end])
            r_squared = r_matrix[0, 1]**2
        else:
            slope, r_squared = np.nan, 0.0

        D2 = slope if r_squared > 0.95 else np.nan
        
        return {
            'r_scales': r_valid, 'correlation_sums': c_valid,
            'log_r': log_r, 'log_C': log_C,
            'D2': D2, 'r_squared': r_squared, 'sample_count': actual_n
        }
