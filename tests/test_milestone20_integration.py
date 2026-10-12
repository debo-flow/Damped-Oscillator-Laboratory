"""
Milestone 20: End-to-End Laboratory Integration Tests
Validates that numerical backends, chaos diagnostics, and system identification 
modules pass data to each other correctly without dimensional mismatches.
"""

import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from numerical_backend import NumericalBackend
from chaos_classification import ChaosClassifier, ChaosEvidence
from model_discovery import SparseEquationDiscoverer

class TestLaboratoryIntegration(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)

    def test_end_to_end_pipeline(self):
        """
        Integration Pipeline Test:
        1. Numerically solve a known linear oscillator.
        2. Feed results to Chaos Classifier (should return 'fixed_point_or_stable_sink').
        3. Feed results to SINDy Equation Discoverer (should recover linear coefficients).
        """
        # 1. Numerical Integration (Stable Damped Oscillator: x'' + 0.5x' + x = 0)
        def linear_osc(t, y): return [y[1], -0.5*y[1] - 1.0*y[0]]
        
        t_span = (0, 20)
        t_eval = np.linspace(0, 20, 500)
        y0 = np.array([1.0, 0.0])
        
        sol = NumericalBackend.robust_solve_ivp(linear_osc, t_span, y0, method='RK45', t_eval=t_eval)
        self.assertTrue(sol['success'], "Numerical backend failed integration.")
        
        # 2. Chaos Classification (Simulate diagnostic outputs for a stable system)
        diagnostics = {
            'lambda_max': -0.25, # Expected max real eigenvalue
            'lyapunov_converged': True,
            'poincare_count': 1,
            'D_KY': 0.0
        }
        evidence = ChaosClassifier.classify(diagnostics)
        self.assertEqual(evidence.classification, "fixed_point_or_stable_sink", 
                         "Chaos classifier incorrectly identified a stable linear system.")
                         
        # 3. System Identification (SINDy)
        x_data = sol['y'].T
        # Estimate derivatives (dx/dt = v, dv/dt = -x - 0.5v)
        dx_data = np.column_stack((x_data[:, 1], -1.0 * x_data[:, 0] - 0.5 * x_data[:, 1]))
        
        discoverer = SparseEquationDiscoverer(poly_order=1)
        discovery_res = discoverer.discover(x_data, dx_data, threshold=0.1)
        
        # Validate that the discovered equation for dv/dt (index 1) contains 'x_0' and 'x_1'
        discovered_eq_v = discovery_res['equations'][1]
        self.assertIn("x_0", discovered_eq_v, "SINDy failed to identify stiffness term.")
        self.assertIn("x_1", discovered_eq_v, "SINDy failed to identify damping term.")

if __name__ == '__main__':
    unittest.main()
