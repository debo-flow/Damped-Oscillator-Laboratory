import unittest
import numpy as np
import sys
import os

# Add the src directory to the path so tests can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from energy_analysis import EnergyAnalyzer
from damped_oscillator import DampedOscillator

class TestEnergyAnalysis(unittest.TestCase):
    def setUp(self):
        self.t = np.linspace(0, 10, 500)
        self.x = np.cos(self.t)
        self.v = -np.sin(self.t)
        self.analyzer = EnergyAnalyzer(m=1.0, b=0.5, k=1.0)
        
    def test_energy_positivity(self):
        """Verifies that U, K, and E never fall strictly below zero."""
        data = self.analyzer.compute_energy_dynamics(self.t, self.x, self.v)
        
        # Allow for tiny floating point inaccuracies around 0
        self.assertTrue(np.all(data['K'] >= -1e-12))
        self.assertTrue(np.all(data['U'] >= -1e-12))
        self.assertTrue(np.all(data['E'] >= -1e-12))

    def test_forces(self):
        """Verifies force logic."""
        data = self.analyzer.compute_energy_dynamics(self.t, self.x, self.v)
        
        # F_s = -kx
        np.testing.assert_array_almost_equal(data['F_s'], -1.0 * self.x)
        # F_d = -bv
        np.testing.assert_array_almost_equal(data['F_d'], -0.5 * self.v)

    def test_energy_conservation_limit(self):
        """Tests the b=0 edge case. Energy must be conserved."""
        # Initialize an undamped oscillator
        osc = DampedOscillator(m=1.0, b=0.0, k=10.0, x0=1.0, v0=0.0)
        res = osc.simulate(rtol=1e-9, atol=1e-11)
        
        analyzer_undamped = EnergyAnalyzer(m=1.0, b=0.0, k=10.0)
        data = analyzer_undamped.compute_energy_dynamics(res['time'], res['displacement'], res['velocity'])
        
        metrics = analyzer_undamped.calculate_metrics(data)
        
        # Dissipated energy and Damping power must be exactly 0
        self.assertTrue(np.allclose(data['P_d'], 0.0))
        self.assertTrue(np.allclose(data['E_diss'], 0.0))
        
        # Energy should be conserved (max deviation less than 1e-5)
        E_0 = data['E'][0]
        max_deviation = np.max(np.abs(data['E'] - E_0))
        self.assertLess(max_deviation, 1e-5)
        
        # Residual should be negligible
        self.assertLess(metrics['max_R_E'], 1e-5)

    def test_damped_energy_balance(self):
        """Tests the energy balance integral E(0) - E(t) = E_diss(t) for a damped system."""
        osc = DampedOscillator(m=1.0, b=0.5, k=10.0, x0=1.0, v0=0.0)
        res = osc.simulate(rtol=1e-9, atol=1e-9)
        
        data = self.analyzer.compute_energy_dynamics(res['time'], res['displacement'], res['velocity'])
        metrics = self.analyzer.calculate_metrics(data)
        
        # Energy balance should hold up to numerical precision of the integration scheme
        self.assertLess(metrics['rms_R_E'], 1e-4)
        
        # Total energy must strictly decrease (or stay flat at 0)
        diff = np.diff(data['E'])
        self.assertTrue(np.all(diff <= 1e-8)) # Allow tiny floating point noise

if __name__ == '__main__':
    unittest.main()
