import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from manifold_analysis import ManifoldPropagator

class TestManifoldAnalysis(unittest.TestCase):
    def test_backward_integration(self):
        """Ensures that stable manifolds propagate backwards in time flawlessly."""
        def simple_decay(t, y, p): return [-y[0]]
        prop = ManifoldPropagator(simple_decay, 1)
        
        # Integrating backwards from a small positive epsilon
        res = prop.propagate_branch(np.array([0.0]), np.array([1.0]), {}, direction='backward', epsilon=0.1, duration=2.0)
        
        # In backward time, a stable trajectory should exponentially GROW away from origin.
        final_x = res['trajectory'][-1, 0]
        self.assertGreater(final_x, 0.1)

if __name__ == '__main__':
    unittest.main()
