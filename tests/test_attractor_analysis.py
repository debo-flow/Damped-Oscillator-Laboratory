import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from attractor_analysis import AttractorAnalyzer

class TestAttractorAnalysis(unittest.TestCase):
    def setUp(self):
        # Create a synthetic 1D line embedded in 2D space (expected dimension approx 1.0)
        t = np.linspace(0, 10, 1000)
        x = t
        v = 2 * t
        self.traj = np.column_stack((x, v))
        self.analyzer = AttractorAnalyzer(self.traj)

    def test_bounding_geometry(self):
        geom = self.analyzer.bounding_geometry()
        self.assertAlmostEqual(geom['min_state'][0], 0.0)
        self.assertAlmostEqual(geom['max_state'][0], 10.0)
        self.assertAlmostEqual(geom['min_state'][1], 0.0)
        self.assertAlmostEqual(geom['max_state'][1], 20.0)

    def test_box_counting_dimension_1D_line(self):
        """Validates that a simple line returns D_box ~ 1.0"""
        res = self.analyzer.box_counting_dimension()
        self.assertTrue(res['r_squared'] > 0.95)
        # Expected to be near 1.0
        self.assertAlmostEqual(res['D_box'], 1.0, places=1)

    def test_correlation_dimension_memory_safeguard(self):
        """Ensures that massively large datasets trigger downsampling without OOM crashing."""
        huge_traj = np.random.rand(10000, 2)
        analyzer = AttractorAnalyzer(huge_traj)
        res = analyzer.correlation_dimension(max_points=2000)
        
        # Ensure it processed a downsampled safe array, not the full 10k
        self.assertLessEqual(res['sample_count'], 2000)

if __name__ == '__main__':
    unittest.main()
