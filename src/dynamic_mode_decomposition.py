"""
Milestone 18: Dynamic Mode Decomposition & Koopman Analysis
Approximates linear evolution operators from nonlinear snapshot data.
"""

import numpy as np
from typing import Dict

class DMDAnalyzer:
    @staticmethod
    def compute_dmd(X: np.ndarray, Y: np.ndarray, rank: int = None) -> Dict:
        """Standard Exact DMD on snapshot matrices X (t) and Y (t+dt)."""
        # SVD of input space
        U, S, Vh = np.linalg.svd(X, full_matrices=False)
        
        if rank is not None:
            U, S, Vh = U[:, :rank], S[:rank], Vh[:rank, :]
            
        V = Vh.T
        S_inv = np.diag(1.0 / S)
        
        # Koopman/A matrix approximation in reduced subspace
        A_tilde = U.T @ Y @ V @ S_inv
        
        # Eigen decomposition
        eigenvalues, W = np.linalg.eig(A_tilde)
        
        # Exact DMD modes
        Phi = Y @ V @ S_inv @ W
        
        # Amplitudes (initial condition projection)
        b = np.linalg.pinv(Phi) @ X[:, 0]
        
        return {
            'eigenvalues': eigenvalues,
            'modes': Phi,
            'amplitudes': b,
            'A_tilde': A_tilde,
            'singular_values': S
        }

    @staticmethod
    def compute_edmd(X: np.ndarray, Y: np.ndarray, dictionary_func) -> Dict:
        """Extended DMD (Koopman approximation) using a lifted feature dictionary."""
        Psi_X = dictionary_func(X.T).T
        Psi_Y = dictionary_func(Y.T).T
        
        # Minimize ||Psi_Y - K Psi_X||_F
        K = Psi_Y @ np.linalg.pinv(Psi_X)
        eigenvalues, eigenvectors = np.linalg.eig(K)
        
        return {
            'K_matrix': K,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors
        }
