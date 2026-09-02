import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from chaos_analysis import ChaosAnalyzer

class TestChaosAnalysis(unittest.TestCase):
    def setUp(self):
        self.omega = np.pi # T_drive = 2 seconds
        self.t = np.linspace(0, 20.0, 1000)
        # Synthetic Period-1 response
        self.x = np.cos(self.omega * self.t)
        self.v = -self.omega * np.sin(self.omega * self.t)
        self.analyzer = ChaosAnalyzer(self.t, self.x, self.v, self.omega)

    def test_driving_period_calculation(self):
        self.assertAlmostEqual(self.analyzer.T_drive, 2.0)

    def test_transient_removal(self):
        self.analyzer.remove_transient(5.0)
        self.assertGreaterEqual(self.analyzer.t[0], 5.0)
        self.assertLess(self.analyzer.t[0], 5.1)

    def test_poincare_stroboscopic_sampling(self):
        """Ensures Poincaré section accurately interpolates periodic synthetic data."""
        poincare = self.analyzer.poincare_section()
        
        # Because x = cos(pi*t), at every t = n*2, x should perfectly equal 1.0
        np.testing.assert_array_almost_equal(poincare['x'], np.ones_like(poincare['x']), decimal=4)
        # And v should perfectly equal 0.0
        np.testing.assert_array_almost_equal(poincare['v'], np.zeros_like(poincare['v']), decimal=4)

    def test_periodic_candidate_detection(self):
        """Validates the clustering algorithm identifies a single cluster for Period-1."""
        poincare = self.analyzer.poincare_section()
        diag = self.analyzer.detect_periodicity(poincare['x'], poincare['v'])
        
        self.assertEqual(diag['estimated_period'], 1)
        self.assertEqual(diag['classification'], 'periodic_candidate')

    def test_recurrence_matrix_generation(self):
        """Tests binary thresholding in recurrence matrices."""
        rm = self.analyzer.recurrence_matrix(epsilon=0.5)
        # The diagonal should always be 1 (distance to self is 0)
        self.assertEqual(rm[0, 0], 1)
        self.assertEqual(rm[-1, -1], 1)

if __name__ == '__main__':
    unittest.main()
