import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from coupled_oscillators import CoupledOscillators
from spectral_analysis import SpectralAnalyzer

class TestCoupledOscillators(unittest.TestCase):
    def setUp(self):
        self.m, self.k, self.kc = 1.0, 10.0, 2.0
        self.sys = CoupledOscillators(self.m, self.m, self.k, self.k, self.kc)

    def test_matrix_construction(self):
        M, C, K = self.sys.get_matrices()
        np.testing.assert_array_almost_equal(M, [[1.0, 0.0], [0.0, 1.0]])
        np.testing.assert_array_almost_equal(C, [[0.0, 0.0], [0.0, 0.0]])
        np.testing.assert_array_almost_equal(K, [[12.0, -2.0], [-2.0, 12.0]])

    def test_analytical_normal_modes(self):
        """Validates numerical eigenvalues against exact analytical formulas for identical oscillators."""
        modes = self.sys.solve_eigenproblem()
        
        w1_theo = np.sqrt(self.k / self.m)
        w2_theo = np.sqrt((self.k + 2*self.kc) / self.m)
        
        self.assertAlmostEqual(modes['omega'][0], w1_theo, places=5)
        self.assertAlmostEqual(modes['omega'][1], w2_theo, places=5)
        
        # Test mode shapes (Symmetric and Antisymmetric)
        # Note: Mode 1 should be proportional to [1, 1], Mode 2 to [1, -1]
        shape1 = modes['mode_shapes'][:, 0]
        shape2 = modes['mode_shapes'][:, 1]
        
        # Ratio of x1 to x2 should be 1 for symmetric, -1 for antisymmetric
        self.assertAlmostEqual(shape1[0]/shape1[1], 1.0, places=5)
        self.assertAlmostEqual(shape2[0]/shape2[1], -1.0, places=5)

    def test_energy_conservation(self):
        """Verifies total mechanical energy remains constant for undamped system."""
        res = self.sys.simulate([1.0, 0.0, 0.0, 0.0], duration=5.0)
        en = self.sys.analyze_energy(res)
        
        E0 = en['E_tot'][0]
        max_deviation = np.max(np.abs(en['E_tot'] - E0))
        self.assertLess(max_deviation, 1e-4)

    def test_no_coupling_equivalence(self):
        """Verifies kc=0 decouples the system exactly."""
        sys_decoupled = CoupledOscillators(m1=1.0, m2=1.0, k1=10.0, k2=20.0, kc=0.0)
        res = sys_decoupled.simulate([1.0, 0.0, 1.0, 0.0], duration=5.0)
        
        # Osc 1 is independent
        w1 = np.sqrt(10.0 / 1.0)
        x1_expected = np.cos(w1 * res['time'])
        np.testing.assert_array_almost_equal(res['x1'], x1_expected, decimal=3)
        
        # Osc 2 is independent
        w2 = np.sqrt(20.0 / 1.0)
        x2_expected = np.cos(w2 * res['time'])
        np.testing.assert_array_almost_equal(res['x2'], x2_expected, decimal=3)

    def test_fft_identifies_normal_frequencies(self):
        """Ensures FFT of a mixed state contains exactly the two normal frequencies."""
        res = self.sys.simulate([1.0, 0.0, 0.0, 0.0], duration=20.0, num_samples=2000)
        analyzer = SpectralAnalyzer(res['time'], res['x1'])
        fft_res = analyzer.compute_fft(window='hann', pad_factor=4)
        
        modes = self.sys.solve_eigenproblem()
        f1_theo = modes['freq_hz'][0]
        f2_theo = modes['freq_hz'][1]
        
        # Detect the two highest peaks
        amps = fft_res['amplitude']
        peaks_indices = np.argsort(amps)[-2:] 
        detected_freqs = sorted([fft_res['frequency_hz'][i] for i in peaks_indices])
        
        # Check against theory (within FFT df resolution)
        self.assertLess(abs(detected_freqs[0] - f1_theo), analyzer.df * 4)
        self.assertLess(abs(detected_freqs[1] - f2_theo), analyzer.df * 4)

if __name__ == '__main__':
    unittest.main()

