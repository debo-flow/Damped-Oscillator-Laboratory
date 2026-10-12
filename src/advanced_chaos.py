"""
Milestone 17: Advanced Chaos, Crisis & Intermittency Orchestration
Orchestrates multi-diagnostic chaos evaluations and global parameter scanning.
"""

import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from chaos_classification import ChaosClassifier
from crisis_analysis import CrisisAnalyzer
from intermittency_analysis import IntermittencyAnalyzer
from transient_chaos import TransientChaosAnalyzer

def export_chaos_report(report: dict, filepath: str):
    """Exports the multi-diagnostic classification report."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"Chaos report exported to {filepath}")

def run_transient_chaos_experiment():
    print("\n--- Transient Chaos & Escape Dynamics Experiment ---")
    # Synthetic escape data representing a chaotic saddle
    np.random.seed(42)
    escape_times = np.random.exponential(scale=50.0, size=200)
    
    t_sorted, p_surv = TransientChaosAnalyzer.survival_function(escape_times)
    fit_res = TransientChaosAnalyzer.fit_exponential_escape(t_sorted, p_surv)
    
    print(f"Detected Escape Rate (kappa): {fit_res['escape_rate_kappa']:.4f}")
    print(f"Exponential Fit Quality (R^2): {fit_res['fit_quality_r2']:.4f}")
    
    plt.figure(figsize=(8, 5))
    plt.plot(t_sorted, p_surv, 'b.', label='Numerical Survival $P(\\tau > t)$')
    if fit_res['is_exponential']:
        t_fit = np.linspace(0, max(t_sorted), 100)
        p_fit = np.exp(-fit_res['escape_rate_kappa'] * t_fit)
        plt.plot(t_fit, p_fit, 'r-', label=f'Fit: $\\kappa = {fit_res["escape_rate_kappa"]:.3f}$')
        
    plt.yscale('log')
    plt.title("Transient Chaos: Escape Time Survival Function")
    plt.xlabel("Time $t$")
    plt.ylabel("Survival Probability (Log Scale)")
    plt.legend(); plt.grid(True)
    plt.tight_layout()
    plt.show()

def mock_system_classification():
    print("\n--- Multi-Diagnostic Chaos Classification ---")
    diagnostics = {
        'lambda_max': 0.15,
        'lyapunov_converged': True,
        'poincare_count': 1500,
        'D_KY': 2.14,
        'transient_chaos': False,
        'crisis_detected': False,
        'intermittency': False
    }
    
    evidence = ChaosClassifier.classify(diagnostics)
    print(f"Final Classification: {evidence.classification.upper()}")
    print(f"Confidence Level:   {evidence.confidence_level.upper()}")
    
    report_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'advanced_chaos', 'chaos_evidence.json')
    export_chaos_report(evidence.to_dict(), report_path)

if __name__ == "__main__":
    run_transient_chaos_experiment()
    mock_system_classification()
