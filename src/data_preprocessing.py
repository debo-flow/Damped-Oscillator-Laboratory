"""
Milestone 18: Data Preprocessing
Generates synthetic trajectories, injects noise, and estimates derivatives.
"""

import numpy as np
from typing import Dict, Tuple

class DataPreprocessor:
    @staticmethod
    def add_gaussian_noise(data: np.ndarray, snr_db: float) -> np.ndarray:
        """Adds Gaussian noise to data based on a Signal-to-Noise Ratio (SNR) in dB."""
        signal_power = np.mean(data**2)
        noise_power = signal_power / (10 ** (snr_db / 10))
        noise = np.random.normal(0, np.sqrt(noise_power), data.shape)
        return data + noise

    @staticmethod
    def estimate_derivatives(t: np.ndarray, x: np.ndarray, method: str = 'finite_difference') -> np.ndarray:
        """Estimates time derivatives of the state trajectory."""
        if method == 'finite_difference':
            dt = np.gradient(t)
            # Handle multi-dimensional state arrays
            if x.ndim == 1:
                return np.gradient(x, dt)
            else:
                return np.array([np.gradient(x[:, i], dt) for i in range(x.shape[1])]).T
        else:
            raise NotImplementedError(f"Derivative method {method} not implemented.")

    @staticmethod
    def split_data(t: np.ndarray, x: np.ndarray, train_ratio: float = 0.8) -> Dict[str, np.ndarray]:
        """Splits time-series data into training and validation sets sequentially."""
        split_idx = int(len(t) * train_ratio)
        return {
            't_train': t[:split_idx], 'x_train': x[:split_idx],
            't_val': t[split_idx:], 'x_val': x[split_idx:]
        }
