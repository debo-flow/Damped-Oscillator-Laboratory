"""
Milestone 20: Master Laboratory Orchestrator
Unified CLI entry point for the Damped-Oscillator-Laboratory.
Routes JSON experiment configurations to the correct scientific modules.
"""

import os
import json
import argparse
import warnings
import numpy as np
from datetime import datetime

# Import Laboratory Modules
from numerical_backend import NumericalBackend
from reproducibility import ReproducibilityTracker
from chaos_analysis import ChaosAnalyzer, run_experiment_preset
from lyapunov_analysis import LyapunovAnalyzer, run_lyapunov_convergence_experiment
from attractor_analysis import AttractorAnalyzer
from bifurcation_analysis import run_equilibrium_continuation_experiment
from global_phase_space import run_duffing_manifold_experiment
from advanced_chaos import run_transient_chaos_experiment
from convergence_analysis import ConvergenceAnalyzer
from system_identification import SystemIdentificationOrchestrator

def setup_environment(seed: int = None):
    """Ensures deterministic execution and handles global warnings."""
    if seed is not None:
        np.random.seed(seed)
    warnings.filterwarnings('ignore', category=UserWarning, module='scipy.integrate')

def execute_experiment(config_path: str):
    """Parses a unified JSON configuration and routes to the appropriate scientific module."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Experiment configuration not found: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    exp_type = config.get('experiment_type', 'unknown')
    print(f"[{datetime.now().strftime('%H:%M:%S')}] INITIALIZING LABORATORY ORCHESTRATOR")
    print(f"Loading Experiment: {os.path.basename(config_path)} (Type: {exp_type.upper()})")

    # Route to the appropriate module based on experiment type
    if exp_type in ['periodic', 'complex', 'period_doubling', 'chaos_analysis']:
        run_experiment_preset(config_path)

    elif exp_type == 'lyapunov_convergence':
        run_lyapunov_convergence_experiment(
            m=config.get('m', 1.0), b=config.get('b', 0.2), 
            k=config.get('k', -1.0), alpha=config.get('alpha', 1.0),
            F0=config.get('F0', 0.3), omega=config.get('omega', 1.2)
        )

    elif exp_type == 'bifurcation_continuation':
        run_equilibrium_continuation_experiment()

    elif exp_type == 'invariant_manifolds':
        run_duffing_manifold_experiment()

    elif exp_type == 'transient_chaos':
        run_transient_chaos_experiment()

    elif exp_type == 'system_identification':
        print("\nRouting to System Identification & Reduced Order Modeling module...")
        # Placeholder for routing to specific System ID JSON configs handled in M18
        pass 

    elif exp_type == 'convergence_analysis':
        print("\nRouting to Tolerance & Convergence Analysis...")
        # Placeholder for routing to specific Convergence configs handled in M19
        pass

    else:
        print(f"ERROR: Unknown experiment_type '{exp_type}'. Please check your JSON configuration.")
        return

    # Generate Reproducibility Manifest
    manifest_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'reproducibility_manifest.json')
    manifest = ReproducibilityTracker.generate_manifest(exp_type, config)
    ReproducibilityTracker.export_manifest(manifest, manifest_path)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] EXPERIMENT COMPLETE. Results and manifest saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Damped Oscillator Laboratory - Unified Orchestrator")
    parser.add_argument('--experiment', type=str, required=True, help="Path to the JSON experiment configuration file.")
    parser.add_argument('--seed', type=int, default=42, help="Random seed for stochastic reproducibility.")
    args = parser.parse_args()

    setup_environment(seed=args.seed)
    execute_experiment(args.experiment)
