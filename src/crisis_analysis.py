"""
Milestone 17: Crisis Detection
Detects Interior (expansion) and Boundary (destruction) crises across parameter sweeps.
"""

import numpy as np
from typing import Dict, List

class CrisisAnalyzer:
    @staticmethod
    def detect_crises(parameters: np.ndarray, attractor_variances: np.ndarray, 
                      escape_rates: np.ndarray, expansion_threshold: float = 2.0) -> List[Dict]:
        """
        Scans parameter sweep data for sudden changes indicating a crisis.
        attractor_variances: Proxy for attractor size/extent.
        escape_rates: Kappa values (0 if bounded, >0 if transient/escaping).
        """
        crises = []
        
        for i in range(1, len(parameters)):
            p_prev, p_curr = parameters[i-1], parameters[i]
            var_prev, var_curr = attractor_variances[i-1], attractor_variances[i]
            esc_prev, esc_curr = escape_rates[i-1], escape_rates[i]
            
            # Boundary Crisis (Attractor suddenly loses stability and trajectories escape)
            if esc_prev == 0.0 and esc_curr > 0.0:
                crises.append({
                    'type': 'boundary_crisis_candidate',
                    'parameter_interval': (p_prev, p_curr),
                    'description': 'Attractor destruction / onset of transient chaos.'
                })
                
            # Interior Crisis (Attractor suddenly expands significantly)
            if var_prev > 0 and (var_curr / var_prev) > expansion_threshold:
                crises.append({
                    'type': 'interior_crisis_candidate',
                    'parameter_interval': (p_prev, p_curr),
                    'description': f'Attractor variance expanded by factor of {var_curr/var_prev:.1f}.'
                })
                
        return crises
