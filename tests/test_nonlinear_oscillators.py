import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from nonlinear_oscillators import DuffingOscillator
from damped_oscillator import DampedOscillator
from forcing import SinusoidalForcing

class TestNonlinearOscillators(unittest.TestCase):
    def setUp(self):
        self.m, self.b, self.k = 1.0, 0.5, 10.0
        self.x0, self.v0 = 1.5, -0.5

    def test_linear_limit_reduction(self):
        """Validates that alpha=0 produces identical results to the pure linear ODE solver."""
        duration = 5.0
        osc_lin = DampedOscillator(self.m, self.b, self.k, self.x0, self.v0, duration=duration)
        res_lin = osc_lin.simulate(rtol=1e-9, atol=1e-9)
        
        osc_duff = DuffingOscillator(self.m, self.b, self.k, alpha=0.0, x0=self.x0, v0=self.v0, duration=duration)
        res_duff = osc_duff.simulate(rtol=1e-9, atol=1e-9)
        
        np.testing.assert_array_almost_equal(res_lin['displacement'], res_duff['x'], decimal=5)
        np.testing.assert_array_almost_equal(res_lin['velocity'], res_duff['v'], decimal=5)

    def test_nonlinear_energy_conservation(self):
        """Verifies total mechanical energy (including 1/4 alpha x^4) is conserved for b=0, F=0."""
        osc = DuffingOscillator(self.m, b=0.0, k=self.k, alpha=2.0, x0=self.x0, v0=self.v0, duration=10.0)
        res = osc.simulate(rtol=1e-10, atol=1e-10)
        
        E0 = res['E_tot'][0]
        max_deviation = np.max(np.abs(res['E_tot'] - E0))
        self.assertLess(max_deviation, 1e-6)

    def test_softening_spring_warning(self):
        """Checks if a negative alpha correctly raises a warning."""
        with self.assertWarns(UserWarning):
            DuffingOscillator(self.m, self.b, self.k, alpha=-1.0)

    def test_forced_energy_balance(self):
        """Validates dE/dt = F(t)*v - b*v^2 for the Duffing system."""
        forcing = SinusoidalForcing(F0=2.0, omega=3.0)
        osc = DuffingOscillator(self.m, self.b, self.k, alpha=1.5, x0=0.0, v0=0.0, 
                                duration=5.0, forcing_function=forcing)
        res = osc.simulate(rtol=1e-9, atol=1e-9)
        
        # Reconstruct work integration
        P_net = res['F_ext'] * res['v'] - self.b * res['v']**2
        from scipy.integrate import cumulative_trapezoid
        Work = cumulative_trapezoid(P_net, res['time'], initial=0.0)
        
        E_calc = res['E_tot'][0] + Work
        max_err = np.max(np.abs(res['E_tot'] - E_calc))
        self.assertLess(max_err, 1e-4)

if __name__ == '__main__':
    unittest.main()

