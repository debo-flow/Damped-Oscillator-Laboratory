"""
Milestone 16: Invariant Sets & Eigenstructure Analysis
Classifies equilibrium points and extracts localized stable/unstable subspaces.
"""

import numpy as np
from typing import Callable, Dict, Tuple
from equilibrium_analysis import EquilibriumAnalyzer

class InvariantSetAnalyzer:
    def __init__(self, analyzer: EquilibriumAnalyzer):
        self.analyzer = analyzer

    def analyze_eigenstructure(self, x_eq: np.ndarray, params: Dict, tol: float = 1e-5) -> Dict:
        """Calculates and categorizes the eigenvalues and eigenvectors of an equilibrium."""
        J = self.analyzer.numerical_jacobian(x_eq, params)
        eigenvalues, eigenvectors = np.linalg.eig(J)
        
        stable_idx, unstable_idx, center_idx = [], [], []
        
        for i, val in enumerate(eigenvalues):
            real_part = np.real(val)
            if real_part < -tol:
                stable_idx.append(i)
            elif real_part > tol:
                unstable_idx.append(i)
            else:
                center_idx.append(i)
                
        hyperbolic = len(center_idx) == 0
        classification = "hyperbolic" if hyperbolic else "non_hyperbolic"
        
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'stable_indices': stable_idx,
            'unstable_indices': unstable_idx,
            'center_indices': center_idx,
            'hyperbolic': hyperbolic,
            'classification': classification
        }
