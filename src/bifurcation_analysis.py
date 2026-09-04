"""
Advanced Bifurcation Analysis & Global Mapping
Orchestrates continuation, Floquet analysis, and global regime mapping.
"""

import numpy as np
import matplotlib.pyplot as plt
from continuation import ContinuationEngine
from equilibrium_analysis import EquilibriumAnalyzer
from periodic_orbit_analysis import PeriodicOrbitAnalyzer

def plot_equilibrium_bifurcation(branch_data: list, param_name: str):
    """Plots a classic bifurcation diagram with stability-colored branches."""
    plt.figure(figsize=(10, 6))
    for pt in branch_data:
        color = 'b' if pt['stability'] == 'stable' else 'r'
        marker = 'o' if pt['event'] == 'none' else '*'
        size = 2 if pt['event'] == 'none' else 10
        plt.scatter(pt['parameter'], pt['state'][0], c=color, s=size, marker=marker)
        
        if pt['event'] != 'none':
            plt.annotate(pt['event'].replace('_', ' ').title(), 
                         (pt['parameter'], pt['state'][0]), textcoords="offset points", xytext=(0,10), ha='center')
            
    plt.title(f"Equilibrium Bifurcation Diagram (Blue=Stable, Red=Unstable)")
    plt.xlabel(f"Control Parameter ({param_name})")
    plt.ylabel("Equilibrium State $x^*$")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def calculate_feigenbaum_ratio(bifurcation_points: list) -> float:
    """Calculates the Feigenbaum ratio delta from sequential period-doubling points."""
    if len(bifurcation_points) < 3:
        return np.nan
    p = bifurcation_points
    return (p[-2] - p[-3]) / (p[-1] - p[-2])

# Example System ODE for testing autonomous equilibria (e.g. Unforced Duffing)
def unforced_duffing(t, y, params):
    x, v = y
    m, b, k, alpha = params['m'], params['b'], params['k'], params['alpha']
    return [v, (-b*v - k*x - alpha*x**3)/m]

def run_equilibrium_continuation_experiment():
    print("\n--- Equilibrium Continuation & Bifurcation Analysis ---")
    analyzer = EquilibriumAnalyzer(unforced_duffing, dimension=2)
    engine = ContinuationEngine(analyzer)
    
    # For a softening spring, we expect multiple equilibria and saddle nodes
    base_params = {'m': 1.0, 'b': 0.2, 'alpha': -1.0}
    
    # Sweep stiffness k
    branch = engine.continue_equilibrium_branch(
        param_name='k', p_start=2.0, p_end=-2.0, 
        initial_guess=np.array([0.0, 0.0]), base_params=base_params,
        dp_init=0.1
    )
    
    events = [pt for pt in branch if pt['event'] != 'none']
    print(f"Total points tracked: {len(branch)}")
    print(f"Candidate Bifurcations detected: {len(events)}")
    for ev in events:
        print(f" - {ev['event']} at k = {ev['parameter']:.4f}")
        
    plot_equilibrium_bifurcation(branch, 'Stiffness (k)')

if __name__ == "__main__":
    run_equilibrium_continuation_experiment()
