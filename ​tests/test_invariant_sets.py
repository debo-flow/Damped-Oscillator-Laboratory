import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from equilibrium_analysis import EquilibriumAnalyzer
from invariant_sets import InvariantSetAnalyzer

class TestInvariantSets(unittest.TestCase):
    def setUp(self):
        # Linear saddle: dx/dt = x, dy/dt = -y
        def linear_saddle(t, y, params): return [y[0], -y[1]]
        self.eq_analyzer = EquilibriumAnalyzer(linear_saddle, 2)
        self.inv_analyzer = InvariantSetAnalyzer(self.eq_analyzer)

    def test_hyperbolic_classification(self):
        res = self.inv_analyzer.analyze_eigenstructure(np.array([0.0, 0.0]), {})
        self.assertTrue(res['hyperbolic'])
        self.assertEqual(len(res['stable_indices']), 1)
        self.assertEqual(len(res['unstable_indices']), 1)
        self.assertEqual(len(res['center_indices']), 0)

if __name__ == '__main__':
    unittest.main()
