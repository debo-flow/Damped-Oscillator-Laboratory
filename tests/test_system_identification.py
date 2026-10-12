import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_preprocessing import DataPreprocessor
from parameter_estimation import ParameterEstimator
from model_discovery import SparseEquationDiscoverer
from reduced_order_model import PODAnalyzer
from system_identification import SystemIdentificationOrchestrator

class TestSystemIdentification(unittest.TestCase):
    def setUp(self):
        self.t = np.linspace(0, 10, 100)
        self.x = np.sin(self.t)
        
    def test_derivative_estimation(self):
        """Tests that finite difference roughly recovers the cosine derivative of sine."""
        dx = DataPreprocessor.estimate_derivatives(self.t, self.x)
        expected_dx = np.cos(self.t)
        # Check interior points (edges suffer from finite diff inaccuracy)
        np.testing.assert_allclose(dx[5:-5], expected_dx[5:-5], atol=0.05)

    def test_noise_injection(self):
        """Verifies SNR calculation mathematically distorts the signal."""
        noisy = DataPreprocessor.add_gaussian_noise(self.x, snr_db=20)
        self.assertFalse(np.array_equal(self.x, noisy))
        self.assertEqual(self.x.shape, noisy.shape)

    def test_parameter_estimation_linear(self):
        """Verifies Least Squares bounds and recovery logic on a trivial linear scale function."""
        def mock_residual(params, t, x_obs):
            A = params[0]
            return (A * t) - x_obs
            
        t_data = np.linspace(0, 5, 10)
        x_data = 2.5 * t_data # True parameter A = 2.5
        
        estimator = ParameterEstimator(mock_residual, ['A'])
        res = estimator.estimate(t_data, x_data, initial_guess=[1.0])
        
        self.assertTrue(res['success'])
        self.assertAlmostEqual(res['estimated_parameters']['A'], 2.5, places=5)
        self.assertEqual(res['identifiability'], 'identifiable_candidate')

    def test_pod_reconstruction(self):
        """Validates SVD energy retention and reconstruction limits."""
        # Create a rank-1 matrix masquerading as 2D
        data = np.vstack((self.x, self.x * 2.0))
        analyzer = PODAnalyzer(data)
        res = analyzer.compute_pod(rank=1)
        
        # A perfectly correlated signal should retain 100% energy in rank 1
        self.assertAlmostEqual(res['retained_energy_fraction'], 1.0, places=5)
        self.assertAlmostEqual(res['reconstruction_error'], 0.0, places=5)

    def test_sindy_sparse_discovery(self):
        """Validates STLSQ thresholding correctly identifies a simple governing law."""
        # dx/dt = -2.0 * x
        x_data = np.expand_dims(np.exp(-2.0 * self.t), axis=1)
        dx_data = -2.0 * x_data
        
        discoverer = SparseEquationDiscoverer(poly_order=1)
        res = discoverer.discover(x_data, dx_data, threshold=0.1)
        
        # Expected Equation: dx_0/dt = -2.0000 * x_0
        self.assertIn("x_0", res['equations'][0])
        self.assertTrue(np.abs(res['coefficients'][1, 0] - (-2.0)) < 1e-4) # Index 1 is x_0

if __name__ == '__main__':
    unittest.main()
