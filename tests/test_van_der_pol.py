import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from van_der_pol import VanDerPolOscillator, extract_limit_cycle_metrics

class TestVanDerPolOscillator(unittest.TestCase):
    def setUp(self):
        self.x0, self.v0 = 1.0, 0.0

    def test_harmonic_limit(self):
        """Validates that mu=0 perfectly reduces to the simple harmonic oscillator x'' + x = 0."""
        sys = VanDerPolOscillator(mu=0.0, x0=self.x0, v0=self.v0, duration=10.0)
        res = sys.simulate(rtol=1e-9, atol=1e-9)
        
        # Analytical solution for x'' + x = 0 with x(0)=1, v(0)=0 is cos(t)
        expected_x = np.cos(res['time'])
        np.testing.assert_array_almost_equal(res['x'], expected_x, decimal=5)

    def test_parameter_validation(self):
        """Ensures invalid mu values (mu < 0) are rejected for the standard model."""
        with self.assertRaises(ValueError):
            VanDerPolOscillator(mu=-1.0)
        with self.assertRaises(ValueError):
            VanDerPolOscillator(duration=0)

    def test_energy_derivative_formula(self):
        """Verifies the energy-like derivative perfectly matches mu*(1-x^2)*v^2."""
        mu = 1.5
        sys = VanDerPolOscillator(mu=mu, x0=2.0, v0=1.0, duration=2.0)
        res = sys.simulate(rtol=1e-8, atol=1e-8)
        
        x = res['x']
        v = res['v']
        expected_dE_dt = mu * (1 - x**2) * v**2
        
        np.testing.assert_array_almost_equal(res['dE_ref_dt'], expected_dE_dt, decimal=6)

    def test_limit_cycle_energy_balance(self):
        """Checks that the cycle-averaged energy growth is approximately zero on the limit cycle."""
        sys = VanDerPolOscillator(mu=0.5, x0=0.1, v0=0.0, duration=100.0)
        # Use a long duration so the last 50% is firmly on the limit cycle
        res = sys.simulate(rtol=1e-7, atol=1e-7)
        
        metrics = extract_limit_cycle_metrics(res['time'], res['x'], res['v'], res['dE_ref_dt'], cutoff_fraction=0.8)
        
        # Mean dE/dt over the cycle should be near zero
        self.assertLess(abs(metrics['cycle_avg_dE_dt']), 5e-3)

if __name__ == '__main__':
    unittest.main()

