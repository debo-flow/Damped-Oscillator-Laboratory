import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from lyapunov_analysis import LyapunovAnalyzer

class TestLyapunovAnalysis(unittest.TestCase):
    def test_numerical_jacobian(self):
        """Tests the finite-difference Jacobian on a known analytical vector field."""
        # Test field: dx/dt = x^2 * y, dy/dt = 3*y
        def test_field(t, state):
            x, y = state
            return [x**2 * y, 3 * y]
        
        analyzer = LyapunovAnalyzer(test_field, dimension=2)
        # Point to evaluate: x=2, y=4
        state = np.array([2.0, 4.0])
        J = analyzer.numerical_jacobian(0.0, state, h=1e-5)
        
        # Analytical Jacobian at (2, 4):
        # [2*x*y, x^2] = [16, 4]
        # [0,       3] = [ 0, 3]
        np.testing.assert_allclose(J[0, 0], 16.0, rtol=1e-4)
        np.testing.assert_allclose(J[0, 1], 4.0, rtol=1e-4)
        np.testing.assert_allclose(J[1, 0], 0.0, atol=1e-4)
        np.testing.assert_allclose(J[1, 1], 3.0, rtol=1e-4)

    def test_stable_lyapunov_convergence(self):
        """Validates that a simple stable linear ODE (dx/dt = -0.5x) returns exactly LLE = -0.5."""
        def stable_decay(t, state):
            return [-0.5 * state[0]]
            
        analyzer = LyapunovAnalyzer(stable_decay, dimension=1)
        res = analyzer.calculate_largest_lyapunov(y0=np.array([1.0]), t_max=20.0, tau_r=1.0, transient_time=0.0)
        
        self.assertTrue(res['converged'])
        self.assertAlmostEqual(res['lyapunov_exponent'], -0.5, places=2)
        self.assertEqual(res['classification'], 'stable_candidate')

    def test_periodic_lyapunov_convergence(self):
        """Validates that a perfect harmonic oscillator (dx/dt = v, dv/dt = -x) returns LLE approx 0."""
        def harmonic_osc(t, state):
            return [state[1], -state[0]]
            
        analyzer = LyapunovAnalyzer(harmonic_osc, dimension=2)
        res = analyzer.calculate_largest_lyapunov(y0=np.array([1.0, 0.0]), t_max=100.0, tau_r=5.0)
        
        self.assertTrue(res['converged'])
        # LLE should be effectively zero for a conservative periodic orbit
        self.assertLess(abs(res['lyapunov_exponent']), 1e-2)
        self.assertEqual(res['classification'], 'periodic_quasiperiodic_candidate')

if __name__ == '__main__':
    unittest.main()
