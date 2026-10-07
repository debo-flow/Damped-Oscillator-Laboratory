"""
Milestone 16: Separatrix & Homoclinic Detection
Detects intersections, boundary proximities, and returning trajectories.
"""

import numpy as np
from typing import Dict, List

class SeparatrixAnalyzer:
    @staticmethod
    def detect_homoclinic_candidate(trajectory: np.ndarray, x_eq: np.ndarray, 
                                    epsilon: float = 5e-2, excursion_min: float = 1.0) -> Dict:
        """Detects if an unstable trajectory returns closely to its originating saddle."""
        dists = np.linalg.norm(trajectory - x_eq, axis=1)
        exited = dists > excursion_min
        
        if not np.any(exited):
            return {'homoclinic_candidate': False, 'reason': 'Did not leave equilibrium neighborhood.'}
            
        exit_idx = np.argmax(exited)
        returned_dists = dists[exit_idx:]
        
        if len(returned_dists) == 0:
            return {'homoclinic_candidate': False, 'reason': 'Trajectory truncated before return.'}
            
        min_return = np.min(returned_dists)
        is_candidate = min_return < epsilon
        
        return {
            'homoclinic_candidate': is_candidate,
            'minimum_return_distance': min_return,
            'outward_excursion': np.max(dists)
        }

    @staticmethod
    def detect_manifold_intersection(traj_a: np.ndarray, traj_b: np.ndarray, tol: float = 1e-2) -> Dict:
        """Detects if two numerical manifold branches cross/intersect."""
        # Highly simplified O(N^2) pairwise distance for intersection candidate detection
        from scipy.spatial.distance import cdist
        # Subsample for memory protection
        step_a = max(1, len(traj_a) // 1000)
        step_b = max(1, len(traj_b) // 1000)
        
        dists = cdist(traj_a[::step_a], traj_b[::step_b])
        min_dist = np.min(dists)
        
        return {
            'intersection_candidate': min_dist < tol,
            'minimum_distance': min_dist
        }
