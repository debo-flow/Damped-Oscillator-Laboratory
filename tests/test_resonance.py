import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from resonance_analysis import ResonanceAnalyzer

class TestResonanceAnalysis(unittest.TestCase):
    def setUp(self):
        # Underdamped system (light damping)
        self.analyzer_light = ResonanceAnalyzer(m=1.0, b=0.2, k=10.0)
        # Heavily damped system (no resonance peak)
        self.analyzer_heavy = ResonanceAnalyzer(m=1.0, b=5.0, k=10.0)

    def test_resonance_frequency_calculation(self):
        """Validates exact w_r formula against w0 * sqrt(1 - 2*zeta^2)."""
        w0 = np.sqrt(10.0)
        zeta = 0.2 / (2 * np.sqrt(10.0))
        expected_wr = w0 * np.sqrt(1 - 2 * zeta**2)
        
        self.assertAlmostEqual(self.analyzer_light.resonance_frequency(), expected_wr, places=5)
        
        # Heavy damping (zeta > 1/sqrt(2)) should return None
        self.assertIsNone(self.analyzer_heavy.resonance_frequency())

    def test_theoretical_amplitude_and_phase(self):
        """Tests frequency response calculations at DC and resonance."""
        w_array = np.array([0.0, np.sqrt(10.0)])
        amp = self.analyzer_light.theoretical_amplitude(w_array, F0=1.0)
        phase = self.analyzer_light.theoretical_phase(w_array)
        
        # At w=0, amplitude should be exactly F0/k (quasi-static limit)
        self.assertAlmostEqual(amp[0], 1.0 / 10.0)
        self.assertAlmostEqual(phase[0], 0.0)
        
        # At natural frequency w0, denominator is just b*w0
        expected_amp_w0 = 1.0 / (0.2 * np.sqrt(10.0))
        self.assertAlmostEqual(amp[1], expected_amp_w0)
        # Phase at natural frequency should be pi/2
        self.assertAlmostEqual(phase[1], np.pi / 2)

    def test_bandwidth_and_quality_factor(self):
        """Verifies bandwidth refinement and Q factor approximations."""
        sweep = self.analyzer_light.frequency_sweep(1.0, 5.0, num_points=5000)
        metrics = self.analyzer_light.refine_resonance(sweep)
        
        # Q_theo = m*w0 / b = 1.0*sqrt(10)/0.2 ≈ 15.81
        q_theo = self.analyzer_light.quality_factor_theoretical()
        
        self.assertIsNotNone(metrics['bandwidth'])
        # Q_num (w_r / bw) should be relatively close to Q_theo for light damping
        self.assertAlmostEqual(metrics['Q_num'], q_theo, delta=0.5)

    def test_zero_damping_singularity(self):
        """Verifies b=0 produces division-by-zero (inf) at natural frequency."""
        undamped = ResonanceAnalyzer(m=1.0, b=0.0, k=10.0)
        w0 = np.sqrt(10.0)
        # Suppress the warning expected for this specific test
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            amp = undamped.theoretical_amplitude(np.array([w0]))
        self.assertEqual(amp[0], np.inf)

if __name__ == '__main__':
    unittest.main()
