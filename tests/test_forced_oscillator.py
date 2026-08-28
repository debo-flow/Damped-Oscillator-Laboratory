import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from damped_oscillator import DampedOscillator
from forcing import SinusoidalForcing
from analytical_solution import AnalyticalSolver
from energy_analysis import EnergyAnalyzer

class TestForcedOscillator(unittest.TestCase):
    def setUp(self):
        self.m, self.b, self.k = 1.0, 0.5, 10.0
        self.F0, self.omega = 2.0, 3.0
        
    def test_parameter_validation(self):
        with self.assertRaises(ValueError):
            SinusoidalForcing(F0=-1.0, omega=2.0)
        with self.assertRaises(ValueError):
            SinusoidalForcing(F0=1.0, omega=-2.0)

    def test_unforced_reduction(self):
        """Verifies F0=0 exactly reproduces unforced Milestone 1-5 behavior."""
        osc_unforced = DampedOscillator(self.m, self.b, self.k, 1.0, 0.0)
        res_u = osc_unforced.simulate(rtol=1e-8, atol=1e-8)
        
        forcing = SinusoidalForcing(0.0, self.omega)
        osc_forced0 = DampedOscillator(self.m, self.b, self.k, 1.0, 0.0, forcing_function=forcing)
        res_f = osc_forced0.simulate(rtol=1e-8, atol=1e-8)
        
        np.testing.assert_array_almost_equal(res_u['displacement'], res_f['displacement'])

    def test_analytical_numerical_agreement(self):
        """Tests if numerical solver matches analytical solution for forced system."""
        forcing = SinusoidalForcing(self.F0, self.omega)
        osc = DampedOscillator(self.m, self.b, self.k, 0.0, 0.0, duration=5.0, forcing_function=forcing)
        num = osc.simulate(rtol=1e-9, atol=1e-9)
        
        ana = AnalyticalSolver(self.m, self.b, self.k, 0.0, 0.0, self.F0, self.omega)
        ana_res = ana.solve(num['time'])
        
        max_err = np.max(np.abs(num['displacement'] - ana_res['displacement']))
        self.assertLess(max_err, 1e-4)

    def test_energy_balance_forced(self):
        """Validates dE/dt = F_drive*v - b*v^2 through the cumulative residual."""
        forcing = SinusoidalForcing(self.F0, self.omega)
        osc = DampedOscillator(self.m, self.b, self.k, 0.0, 0.0, duration=5.0, forcing_function=forcing)
        num = osc.simulate(rtol=1e-9, atol=1e-9)
        
        ea = EnergyAnalyzer(self.m, self.b, self.k)
        en = ea.compute_energy_dynamics(num['time'], num['displacement'], num['velocity'], num['external_force'])
        
        self.assertLess(np.max(np.abs(en['R_E'])), 1e-4)

if __name__ == '__main__':
    unittest.main()
