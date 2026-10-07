import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from separatrix_analysis import SeparatrixAnalyzer

class TestSeparatrixAnalysis(unittest.TestCase):
    def test_homoclinic_candidate_detection(self):
        """Validates the logic recognizing a trajectory that leaves and returns."""
        # Synthetic trajectory that leaves origin, goes to 2, and returns to 0.01
        t = np.linspace(0, np.pi, 100)
        traj = np.column_stack((2 * np.sin(t), 2 * np.cos(t)))
        
        # Ensure start and end are near 0
        traj[0] = [0.001, 0.0]
        traj[-1] = [0.001, 0.0]
        
        res = SeparatrixAnalyzer.detect_homoclinic_candidate(traj, np.array([0.0, 0.0]), epsilon=0.05, excursion_min=1.0)
        self.assertTrue(res['homoclinic_candidate'])

if __name__ == '__main__':
    unittest.main()
