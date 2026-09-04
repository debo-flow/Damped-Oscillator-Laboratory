"""
Adaptive Parameter Continuation Engine
Tracks branches continuously, implementing forward/backward stepping and adaptive resolution.
"""

import numpy as np
from typing import Dict, List, Optional
from equilibrium_analysis import EquilibriumAnalyzer

class ContinuationEngine:
    def __init__(self, analyzer: EquilibriumAnalyzer):
        self.analyzer = analyzer

    def continue_equilibrium_branch(self, param_name: str, p_start: float, p_end: float, 
                                    initial_guess: np.ndarray, base_params: Dict,
                                    dp_init: float = 0.05, dp_min: float = 1e-4, dp_max: float = 0.2) -> List[Dict]:
        """Tracks equilibrium states across a parameter range."""
        branch_data = []
        p_curr = p_start
        dp = dp_init if p_end > p_start else -dp_init
        direction = 1 if p_end > p_start else -1
        current_guess = np.copy(initial_guess)
        
        while (p_curr <= p_end if direction == 1 else p_curr >= p_end):
            params = base_params.copy()
            params[param_name] = p_curr
            
            eq_res = self.analyzer.find_equilibrium(current_guess, params)
            
            if eq_res['converged']:
                stab_res = self.analyzer.analyze_stability(eq_res['equilibrium_state'], params)
                
                branch_data.append({
                    'parameter': p_curr,
                    'state': eq_res['equilibrium_state'],
                    'residual': eq_res['residual_norm'],
                    'eigenvalues': stab_res['eigenvalues'],
                    'max_real_part': stab_res['max_real_part'],
                    'stability': stab_res['stability'],
                    'event': stab_res['event']
                })
                
                current_guess = eq_res['equilibrium_state']
                dp = np.clip(dp * 1.2, -dp_max, dp_max) if direction == 1 else np.clip(dp * 1.2, -dp_max, dp_max)
                p_curr += dp
            else:
                # Step size collapse
                dp *= 0.5
                if abs(dp) < dp_min:
                    print(f"Branch terminated at {param_name} = {p_curr}: Minimum step size reached.")
                    break
                    
        return branch_data

