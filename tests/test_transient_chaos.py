import unittest
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from transient_chaos import TransientChaosAnalyzer

class TestTransientChaos(unittest.TestCase):
    def test_escape_detection(self):
        traj = np.array([[0,0], [1,1], [15, 15], [20, 20]])
        idx = TransientChaosAnalyzer.detect_escape(traj, boundary_threshold=10.0)
        self.assertEqual(idx, 2) # Escapes at index 2

    def test_exponential_fit(self):
        t = np.linspace(0, 10, 50)
        p = np.exp(-0.5 * t)
        res = TransientChaosAnalyzer.fit_exponential_escape(t, p)
        self.assertAlmostEqual(res['escape_rate_kappa'], 0.5, places=3)
        self.assertTrue(res['is_exponential'])

if __name__ == '__main__':
    unittest.main()
