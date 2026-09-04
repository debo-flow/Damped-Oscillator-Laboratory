"""
Branch Tracking & Basin Sampling
Groups multistable attractors and calculates basic basin-of-attraction geometries.
"""

import numpy as np
from typing import Callable, Dict, List

class BasinMapper:
    def __init__(self, simulate_func: Callable):
        """simulate_func should take y0 and return the final steady-state phase-space point."""
        self.simulate_func = simulate_func
        self.attractors = []

    def _classify_attractor(self, final_state: np.ndarray, tol: float = 1e-2) -> int:
        for i, attractor in enumerate(self.attractors):
            if np.linalg.norm(final_state - attractor) < tol:
                return i
        self.attractors.append(final_state)
        return len(self.attractors) - 1

    def sample_basin(self, x_range: Tuple[float, float], v_range: Tuple[float, float], 
                     resolution: int = 20) -> Dict:
        """Scans a 2D grid of initial conditions to map the basin of attraction."""
        x_vals = np.linspace(x_range[0], x_range[1], resolution)
        v_vals = np.linspace(v_range[0], v_range[1], resolution)
        
        basin_map = np.zeros((resolution, resolution), dtype=int)
        
        for i, v0 in enumerate(v_vals):
            for j, x0 in enumerate(x_vals):
                try:
                    final_state = self.simulate_func([x0, v0])
                    attractor_id = self._classify_attractor(final_state)
                    basin_map[i, j] = attractor_id
                except Exception:
                    basin_map[i, j] = -1 # Integration failure / divergence
                    
        return {
            'x_grid': x_vals,
            'v_grid': v_vals,
            'basin_map': basin_map,
            'unique_attractors': len(self.attractors)
        }

