import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from chaos_classification import ChaosClassifier

class TestChaosClassification(unittest.TestCase):
    def test_strongly_supported_chaos(self):
        diag = {'lambda_max': 0.2, 'lyapunov_converged': True, 'poincare_count': 500, 'D_KY': 2.1}
        ev = ChaosClassifier.classify(diag)
        self.assertEqual(ev.classification, "strongly_supported_chaos")
        self.assertEqual(ev.confidence_level, "high")
        
    def test_periodic_window(self):
        diag = {'lambda_max': -0.0001, 'lyapunov_converged': True, 'poincare_count': 3, 'in_chaotic_region': True}
        ev = ChaosClassifier.classify(diag)
        self.assertEqual(ev.classification, "periodic_window")
        
    def test_uncertain_convergence(self):
        diag = {'lambda_max': 0.5, 'lyapunov_converged': False}
        ev = ChaosClassifier.classify(diag)
        self.assertEqual(ev.classification, "numerically_uncertain")

if __name__ == '__main__':
    unittest.main()
