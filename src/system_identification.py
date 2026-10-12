"""
Milestone 18: System Identification & Validation Orchestrator
Coordinates parameter estimation, SINDy, DMD, ROM, and generates validation reports.
"""

import os
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any

class SystemIdentificationOrchestrator:
    @staticmethod
    def calculate_residuals(x_true: np.ndarray, x_pred: np.ndarray) -> Dict:
        """Calculates diagnostic errors between observed and model-predicted trajectories."""
        res = x_true - x_pred
        return {
            'rmse': np.sqrt(np.mean(res**2)),
            'mae': np.mean(np.abs(res)),
            'max_error': np.max(np.abs(res)),
            'residual_variance': np.var(res),
            'residuals': res
        }

    @staticmethod
    def plot_validation(t: np.ndarray, x_obs: np.ndarray, x_pred: np.ndarray, title: str):
        """Generates scientific plots comparing true data with identified model predictions."""
        res = x_obs - x_pred
        
        fig, axs = plt.subplots(2, 1, figsize=(10, 8))
        fig.suptitle(title)
        
        axs[0].plot(t, x_obs, 'k-', label='Observed Data', alpha=0.6)
        axs[0].plot(t, x_pred, 'r--', label='Model Prediction')
        axs[0].set_ylabel('State')
        axs[0].legend(); axs[0].grid(True)
        
        axs[1].plot(t, res, 'b-', label='Residual Error')
        axs[1].set_ylabel('Error')
        axs[1].set_xlabel('Time')
        axs[1].legend(); axs[1].grid(True)
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def export_report(report_data: Dict[str, Any], filename: str):
        """Exports the system identification report to JSON."""
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'system_identification'), exist_ok=True)
        filepath = os.path.join(os.path.dirname(__file__), '..', 'results', 'system_identification', f"{filename}.json")
        
        # Ensure numpy arrays are converted to lists for JSON serialization
        def default_serializer(obj):
            if isinstance(obj, np.ndarray): return obj.tolist()
            if isinstance(obj, (np.int64, np.int32)): return int(obj)
            if isinstance(obj, (np.float64, np.float32)): return float(obj)
            raise TypeError
            
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=4, default=default_serializer)
        print(f"System ID Report exported to {filepath}")
