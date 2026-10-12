"""
Milestone 18: Model Discovery & Sparse Equation Identification
Discovers governing analytical equations from trajectory data.
"""

import numpy as np
from typing import Dict, List

class SparseEquationDiscoverer:
    def __init__(self, poly_order: int = 3, use_sine: bool = False):
        self.poly_order = poly_order
        self.use_sine = use_sine
        self.feature_names = []

    def build_feature_library(self, x: np.ndarray) -> np.ndarray:
        """Constructs a library matrix Theta(X) of candidate nonlinear functions."""
        samples, dims = x.shape
        features = [np.ones((samples, 1))]
        self.feature_names = ['1']
        
        # Linear
        for i in range(dims):
            features.append(x[:, i:i+1])
            self.feature_names.append(f"x_{i}")
            
        # Quadratic
        if self.poly_order >= 2:
            for i in range(dims):
                for j in range(i, dims):
                    features.append((x[:, i] * x[:, j]).reshape(-1, 1))
                    self.feature_names.append(f"x_{i}*x_{j}")
                    
        # Cubic
        if self.poly_order >= 3:
            for i in range(dims):
                features.append((x[:, i]**3).reshape(-1, 1))
                self.feature_names.append(f"x_{i}^3")
                
        # Sine
        if self.use_sine:
            for i in range(dims):
                features.append(np.sin(x[:, i:i+1]))
                self.feature_names.append(f"sin(x_{i})")
                
        return np.hstack(features)

    def sparsify_dynamics(self, Theta: np.ndarray, dX: np.ndarray, threshold: float = 0.1, max_iter: int = 10) -> np.ndarray:
        """Sequential Thresholded Least Squares (STLSQ)."""
        Xi = np.linalg.lstsq(Theta, dX, rcond=None)[0]
        
        for _ in range(max_iter):
            small_inds = np.abs(Xi) < threshold
            Xi[small_inds] = 0
            
            for j in range(dX.shape[1]):
                big_inds = ~small_inds[:, j]
                if np.sum(big_inds) > 0:
                    Xi[big_inds, j] = np.linalg.lstsq(Theta[:, big_inds], dX[:, j], rcond=None)[0]
        return Xi

    def discover(self, x: np.ndarray, dx: np.ndarray, threshold: float = 0.1) -> Dict:
        Theta = self.build_feature_library(x)
        Xi = self.sparsify_dynamics(Theta, dx, threshold)
        
        equations = []
        for j in range(Xi.shape[1]):
            terms = [f"{Xi[i, j]:.4f} * {self.feature_names[i]}" for i in range(Xi.shape[0]) if Xi[i, j] != 0]
            eq = " + ".join(terms) if terms else "0"
            equations.append(f"dx_{j}/dt = {eq}")
            
        return {
            'coefficients': Xi,
            'equations': equations,
            'feature_names': self.feature_names
        }
