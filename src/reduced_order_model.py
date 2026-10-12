"""
Milestone 18: Reduced-Order Modeling (POD)
Compresses high-dimensional state trajectories using Proper Orthogonal Decomposition.
"""

import numpy as np
from typing import Dict

class PODAnalyzer:
    def __init__(self, data: np.ndarray):
        """data: snapshot matrix of shape (features, samples)"""
        self.data = data
        self.U = None
        self.S = None
        self.Vh = None

    def compute_pod(self, rank: int) -> Dict:
        """Calculates the optimal rank-r basis using SVD."""
        if self.U is None:
            self.U, self.S, self.Vh = np.linalg.svd(self.data, full_matrices=False)
            
        U_r = self.U[:, :rank]
        
        # Project into reduced coordinates
        z = U_r.T @ self.data
        
        # Reconstruct into original space
        x_recon = U_r @ z
        
        # Energy retained
        total_energy = np.sum(self.S**2)
        retained_energy = np.sum(self.S[:rank]**2) / total_energy
        
        reconstruction_error = np.linalg.norm(self.data - x_recon, 'fro') / np.linalg.norm(self.data, 'fro')
        
        return {
            'reduced_basis': U_r,
            'reduced_trajectory': z,
            'reconstructed_trajectory': x_recon,
            'singular_values': self.S,
            'retained_energy_fraction': retained_energy,
            'reconstruction_error': reconstruction_error
        }
