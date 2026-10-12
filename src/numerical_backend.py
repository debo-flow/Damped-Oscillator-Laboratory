"""
Milestone 19: High-Performance Numerical Backend
Provides solver selection, memory safeguards, and robust IVP integration.
"""

import warnings
import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Dict, Any, Tuple

class NumericalBackend:
    SUPPORTED_SOLVERS = ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA']

    @staticmethod
    def recommend_solver(is_stiff: bool = False, high_precision: bool = False) -> str:
        """Advises on the best solver based on system characteristics."""
        if is_stiff:
            return 'BDF' if not high_precision else 'Radau'
        else:
            return 'DOP853' if high_precision else 'RK45'

    @staticmethod
    def robust_solve_ivp(fun: Callable, t_span: Tuple[float, float], y0: np.ndarray,
                         method: str = 'RK45', rtol: float = 1e-6, atol: float = 1e-8,
                         max_samples: int = 1000000, t_eval: np.ndarray = None, 
                         **kwargs) -> Dict[str, Any]:
        """
        Integrates an ODE system with memory safeguards and detailed status reporting.
        """
        if method not in NumericalBackend.SUPPORTED_SOLVERS:
            warnings.warn(f"Method {method} not standard. Falling back to RK45.")
            method = 'RK45'

        # Memory Safeguard: Prevent OOM on extremely dense t_eval requests
        if t_eval is not None and len(t_eval) > max_samples:
            warnings.warn(f"Requested {len(t_eval)} samples exceeds max_samples={max_samples}. Downsampling.")
            step = len(t_eval) // max_samples
            t_eval = t_eval[::step]

        try:
            sol = solve_ivp(fun, t_span, y0, method=method, t_eval=t_eval, 
                            rtol=rtol, atol=atol, **kwargs)
        except Exception as e:
            return {'success': False, 'status': 'exception', 'message': str(e)}

        return {
            'success': sol.success,
            'status': sol.status,
            'message': sol.message,
            't': sol.t,
            'y': sol.y,
            'nfev': sol.nfev,
            'njev': sol.njev,
            'nlu': sol.nlu,
            'method_used': method
        }
