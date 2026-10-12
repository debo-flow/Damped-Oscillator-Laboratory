"""
Milestone 19: Convergence Analysis
Evaluates trajectory and Lyapunov exponent convergence across shrinking numerical tolerances.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Dict
from numerical_backend import NumericalBackend

class ConvergenceAnalyzer:
    @staticmethod
    def run_tolerance_study(fun: Callable, t_span: tuple, y0: np.ndarray, 
                            tolerances: List[float], method: str = 'RK45') -> Dict:
        """Integrates the same system at progressively tighter tolerances to observe convergence."""
        results = []
        t_eval = np.linspace(t_span[0], t_span[1], 5000)
        
        # Use the tightest tolerance as the "ground truth" reference
        ref_tol = tolerances[-1] * 0.1
        ref_sol = NumericalBackend.robust_solve_ivp(fun, t_span, y0, method=method, 
                                                    rtol=ref_tol, atol=ref_tol, t_eval=t_eval)
        y_ref = ref_sol['y']
        
        for tol in tolerances:
            sol = NumericalBackend.robust_solve_ivp(fun, t_span, y0, method=method, 
                                                    rtol=tol, atol=tol, t_eval=t_eval)
            
            err = np.sqrt(np.mean((sol['y'] - y_ref)**2)) if sol['success'] else np.nan
            results.append({
                'tol': tol,
                'rmse': err,
                'nfev': sol['nfev'],
                'success': sol['success']
            })
            
        return {'reference_tol': ref_tol, 'study': results}

    @staticmethod
    def plot_convergence(results: Dict):
        tols = [r['tol'] for r in results['study']]
        rmses = [r['rmse'] for r in results['study']]
        
        plt.figure(figsize=(8, 5))
        plt.loglog(tols, rmses, 'bo-', label='RMSE vs Reference')
        plt.gca().invert_xaxis() # Tighter tolerance to the right
        plt.title("Numerical Convergence Study")
        plt.xlabel("Tolerance (rtol=atol)")
        plt.ylabel("Root Mean Square Error")
        plt.grid(True, which="both", ls="--")
        plt.legend()
        plt.tight_layout()
        plt.show()
