import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from spectral_analysis import SpectralAnalyzer

class TestSpectralAnalysis(unittest.TestCase):
    def setUp(self):
        # 10 seconds of 5 Hz sine wave, amplitude 2.0, uniformly sampled at 100 Hz
        self.fs = 100.0
        self.t = np.arange(0, 10.0, 1.0/self.fs)
        self.f_signal = 5.0
        self.amp = 2.0
        self.x = self.amp * np.cos(2 * np.pi * self.f_signal * self.t)
        self.analyzer = SpectralAnalyzer(self.t, self.x)

    def test_uniform_sampling_validation(self):
        """Ensures non-uniform time grids throw a ValueError."""
        t_non_uniform = np.array([0.0, 0.1, 0.2, 0.35, 0.4]) # 0.35 breaks uniform step
        x_dummy = np.zeros_like(t_non_uniform)
        with self.assertRaises(ValueError):
            SpectralAnalyzer(t_non_uniform, x_dummy)

    def test_sampling_parameters(self):
        """Validates fs, Nyquist, and frequency resolution (df)."""
        self.assertAlmostEqual(self.analyzer.fs, 100.0)
        self.assertAlmostEqual(self.analyzer.nyquist, 50.0)
        
        expected_df = self.fs / len(self.t)
        self.assertAlmostEqual(self.analyzer.df, expected_df)

    def test_fft_amplitude_and_frequency(self):
        """Tests that a pure sine wave maps exactly to correct bin with correct amplitude."""
        fft_data = self.analyzer.compute_fft(window='boxcar')
        dom = self.analyzer.detect_dominant_frequency(fft_data)
        
        self.assertAlmostEqual(dom['dominant_frequency_hz'], self.f_signal)
        # Check amplitude normalization (should match 2.0)
        self.assertAlmostEqual(dom['peak_amplitude'], self.amp, places=2)

    def test_transient_removal(self):
        """Tests slicing the time array."""
        self.analyzer.remove_transient(cutoff_time=5.0)
        self.assertAlmostEqual(self.analyzer.t[0], 5.0)
        self.assertAlmostEqual(self.analyzer.duration, 5.0 - (1/self.fs)) # 5 secs remaining

    def test_aliasing_prediction(self):
        """Tests that undersampling causes predictable aliasing."""
        # 12 Hz signal sampled at 15 Hz. Expected alias = |12 - 15| = 3 Hz
        t_bad = np.arange(0, 5.0, 1.0/15.0)
        x_bad = np.cos(2 * np.pi * 12.0 * t_bad)
        bad_analyzer = SpectralAnalyzer(t_bad, x_bad)
        
        fft_data = bad_analyzer.compute_fft(window='boxcar')
        dom = bad_analyzer.detect_dominant_frequency(fft_data)
        
        self.assertAlmostEqual(dom['dominant_frequency_hz'], 3.0)

if __name__ == '__main__':
    unittest.main()
