"""
Milestone 16: Invariant Manifold Propagation
Approximates global stable and unstable manifolds via numerical integration.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Dict, List
from invariant_sets import InvariantSetAnalyzer

class ManifoldPropagator:
    def __init__(self, ode_func: Callable, dimension: int):
        self.ode_func = ode_func
        self.dimension = dimension

    def _calculate_arc_length(self, trajectory: np.ndarray) -> np.ndarray:
        diffs = np.diff(trajectory, axis=0)
        lengths = np.linalg.norm(diffs, axis=1)
        return np.concatenate(([0.0], np.cumsum(lengths)))

    def _calculate_curvature_2d(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        dx, dy = np.gradient(x), np.gradient(y)
        ddx, ddy = np.gradient(dx), np.gradient(dy)
        denom = (dx**2 + dy**2)**1.5
        denom[denom == 0] = np.inf
        return np.abs(dx * ddy - dy * ddx) / denom

    def propagate_branch(self, x_eq: np.ndarray, eigenvector: np.ndarray, params: Dict,
                         direction: str = 'forward', epsilon: float = 1e-4, 
                         duration: float = 20.0, num_samples: int = 2000, sign: int = 1) -> Dict:
        """
        Integrates a manifold branch. 
        Unstable manifolds integrate 'forward'. Stable manifolds integrate 'backward'.
        """
        v = np.real(eigenvector)
        v = v / np.linalg.norm(v)
        x0 = x_eq + sign * epsilon * v
        
        t_span = (0.0, duration) if direction == 'forward' else (0.0, -duration)
        t_eval = np.linspace(t_span[0], t_span[1], num_samples)
        
        sol = solve_ivp(self.ode_func, t_span, x0, args=(params,), t_eval=t_eval, 
                        method='RK45', rtol=1e-8, atol=1e-8)
        
        traj = sol.y.T
        arc_lengths = self._calculate_arc_length(traj)
        
        curvature = np.zeros(len(traj))
        if self.dimension == 2:
            curvature = self._calculate_curvature_2d(traj[:, 0], traj[:, 1])
            
        termination = "reached_max_time" if sol.success else "numerical_divergence"
        
        return {
            'time': sol.t,
            'trajectory': traj,
            'arc_length': arc_lengths,
            'curvature': curvature,
            'max_curvature': np.max(curvature) if len(curvature) > 0 else 0.0,
            'termination_reason': termination
        }
        
    def compute_1d_manifold(self, x_eq: np.ndarray, eigenvector: np.ndarray, params: Dict,
                            manifold_type: str = 'unstable', epsilon: float = 1e-4, 
                            duration: float = 20.0) -> Dict:
        """Computes both the positive and negative branches of a 1D manifold."""
        direction = 'forward' if manifold_type == 'unstable' else 'backward'
        
        branch_plus = self.propagate_branch(x_eq, eigenvector, params, direction, epsilon, duration, sign=1)
        branch_minus = self.propagate_branch(x_eq, eigenvector, params, direction, epsilon, duration, sign=-1)
        
        return {'positive_branch': branch_plus, 'negative_branch': branch_minus, 'type': manifold_type}
