import unittest
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from crisis_analysis import CrisisAnalyzer

class TestCrisisAnalysis(unittest.TestCase):
    def test_interior_crisis_detection(self):
        params = np.array([0.1, 0.2, 0.3])
        variances = np.array([1.0, 1.1, 5.0]) # Sudden jump at 0.3
        escapes = np.array([0.0, 0.0, 0.0])
        
        crises = CrisisAnalyzer.detect_crises(params, variances, escapes, expansion_threshold=2.0)
        self.assertEqual(len(crises), 1)
        self.assertEqual(crises[0]['type'], 'interior_crisis_candidate')
        self.assertEqual(crises[0]['parameter_interval'], (0.2, 0.3))

if __name__ == '__main__':
    unittest.main()
