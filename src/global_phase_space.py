"""
Milestone 16: Global Phase-Space Structure Map
Synthesizes invariant sets, manifolds, and separatrices into a global geometric object.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
from equilibrium_analysis import EquilibriumAnalyzer
from invariant_sets import InvariantSetAnalyzer
from manifold_analysis import ManifoldPropagator
from separatrix_analysis import SeparatrixAnalyzer

class GlobalPhaseSpaceMap:
    def __init__(self):
        self.equilibria = []
        self.manifolds = []
        self.homoclinic_candidates = []

    def export_summary(self, filepath: str):
        summary = {
            'equilibria_count': len(self.equilibria),
            'manifolds_computed': len(self.manifolds),
            'homoclinic_candidates': len(self.homoclinic_candidates)
        }
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=4)

def run_duffing_manifold_experiment():
    print("\n--- Global Phase-Space & Separatrix Experiment (Double-Well Duffing) ---")
    
    def unforced_duffing(t, y, params):
        x, v = y
        return [v, (-params['b']*v - params['k']*x - params['alpha']*x**3)/params['m']]
        
    params = {'m': 1.0, 'b': 0.15, 'k': -1.0, 'alpha': 1.0}
    
    eq_analyzer = EquilibriumAnalyzer(unforced_duffing, 2)
    inv_analyzer = InvariantSetAnalyzer(eq_analyzer)
    propagator = ManifoldPropagator(unforced_duffing, 2)
    
    # 1. Analyze Saddle at Origin
    x_saddle = np.array([0.0, 0.0])
    eigen_data = inv_analyzer.analyze_eigenstructure(x_saddle, params)
    print(f"Origin Classification: {eigen_data['classification']}")
    
    v_stable = eigen_data['eigenvectors'][:, eigen_data['stable_indices'][0]]
    v_unstable = eigen_data['eigenvectors'][:, eigen_data['unstable_indices'][0]]
    
    # 2. Propagate Manifolds
    print("Propagating Global Manifolds (Numerical Approximation)...")
    w_s = propagator.compute_1d_manifold(x_saddle, v_stable, params, 'stable', duration=15.0)
    w_u = propagator.compute_1d_manifold(x_saddle, v_unstable, params, 'unstable', duration=15.0)
    
    # 3. Detect Homoclinic/Heteroclinic Connections
    homo_check = SeparatrixAnalyzer.detect_homoclinic_candidate(w_u['positive_branch']['trajectory'], x_saddle)
    print(f"Homoclinic Candidate Detected: {homo_check['homoclinic_candidate']}")
    
    # Visualization
    plt.figure(figsize=(10, 6))
    
    # Stable Manifold (Inflowing)
    plt.plot(w_s['positive_branch']['trajectory'][:, 0], w_s['positive_branch']['trajectory'][:, 1], 'b-', label='$W^s$ (Stable)')
    plt.plot(w_s['negative_branch']['trajectory'][:, 0], w_s['negative_branch']['trajectory'][:, 1], 'b-')
    
    # Unstable Manifold (Outflowing)
    plt.plot(w_u['positive_branch']['trajectory'][:, 0], w_u['positive_branch']['trajectory'][:, 1], 'r-', label='$W^u$ (Unstable)')
    plt.plot(w_u['negative_branch']['trajectory'][:, 0], w_u['negative_branch']['trajectory'][:, 1], 'r-')
    
    # Plot Saddle
    plt.plot(0, 0, 'ko', markersize=8, label='Saddle Equilibrium')
    
    plt.title("Global Phase-Space Invariant Manifolds (Double-Well Duffing)")
    plt.xlabel("Displacement $x$"); plt.ylabel("Velocity $v$")
    plt.xlim(-2, 2); plt.ylim(-2, 2)
    plt.legend(); plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_duffing_manifold_experiment()
