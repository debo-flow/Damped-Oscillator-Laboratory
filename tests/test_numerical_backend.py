import unittest
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from numerical_backend import NumericalBackend
from numerical_validation import NumericalValidator

class TestNumericalValidation(unittest.TestCase):
    def test_analytical_linear_oscillator(self):
        """Tests RK45 against the exact analytical solution for an undamped oscillator."""
        # ODE: x'' + x = 0  => x(t) = cos(t), v(t) = -sin(t)
        def harmonic_ode(t, y): return [y[1], -y[0]]
        
        t_span = (0, 10)
        t_eval = np.linspace(0, 10, 100)
        y0 = np.array([1.0, 0.0])
        
        sol = NumericalBackend.robust_solve_ivp(harmonic_ode, t_span, y0, method='RK45', t_eval=t_eval)
        
        exact_x = np.cos(t_eval)
        errors = NumericalValidator.calculate_errors(sol['y'][0], exact_x)
        
        # Error should be microscopic
        self.assertLess(errors['rmse'], 1e-4)
        
    def test_memory_safeguard(self):
        """Ensures the backend gracefully downsamples rather than allowing OOM arrays."""
        def dummy_ode(t, y): return [-y[0]]
        
        t_span = (0, 1)
        t_eval = np.linspace(0, 1, 5000) # Request 5000 points
        
        # Restrict backend to 1000 max points
        sol = NumericalBackend.robust_solve_ivp(dummy_ode, t_span, [1.0], max_samples=1000, t_eval=t_eval)
        
        self.assertLessEqual(len(sol['t']), 1000)

    def test_energy_balance(self):
        """Tests physical energy conservation residual calculations."""
        t = np.linspace(0, 5, 500)
        # Synthetic decaying trajectory
        x = np.exp(-0.1*t) * np.cos(t)
        v = -0.1*np.exp(-0.1*t)*np.cos(t) - np.exp(-0.1*t)*np.sin(t)
        
        res = NumericalValidator.validate_energy_balance(t, x, v, m=1.0, k=1.0, c=0.2)
        
        # Residuals should be near zero if integration is tight
        self.assertLess(res['max_residual'], 0.05)

if __name__ == '__main__':
    unittest.main()
