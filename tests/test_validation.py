import unittest
import numpy as np
import sys
import os

# Add the src directory to the path so tests can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from damped_oscillator import DampedOscillator
from analytical_solution import AnalyticalSolver

class TestOscillatorValidation(unittest.TestCase):
    def setUp(self):
        self.t = np.linspace(0, 5, 100)
        
    def test_initial_conditions(self):
        solver = AnalyticalSolver(m=1.0, b=0.5, k=10.0, x0=1.5, v0=-0.5)
        res = solver.solve(np.array([0.0]))
        self.assertAlmostEqual(res['displacement'][0], 1.5, places=5)
        self.assertAlmostEqual(res['velocity'][0], -0.5, places=5)

    def test_numerical_stability(self):
        osc = DampedOscillator(m=1.0, b=0.5, k=10.0, x0=1.0, v0=0.0)
        res = osc.simulate()
        self.assertTrue(np.all(np.isfinite(res['displacement'])))
        self.assertTrue(np.all(np.isfinite(res['velocity'])))

    def test_analytical_numerical_agreement(self):
        m, b, k, x0, v0 = 1.0, 0.5, 10.0, 1.0, 0.0
        osc = DampedOscillator(m, b, k, x0, v0, duration=5, num_samples=500)
        ana = AnalyticalSolver(m, b, k, x0, v0)
        
        num_res = osc.simulate(rtol=1e-7, atol=1e-9)
        ana_res = ana.solve(num_res['time'])
        
        max_err = np.max(np.abs(num_res['displacement'] - ana_res['displacement']))
        self.assertLess(max_err, 1e-4)

if __name__ == '__main__':
    unittest.main()

