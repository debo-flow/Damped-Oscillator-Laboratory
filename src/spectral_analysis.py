"""
Milestone 8: FFT & Frequency-Domain Analysis Laboratory
Analyzes the spectral content of oscillator signals using FFT and PSD.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window, welch
from typing import Dict, Tuple, Optional
from damped_oscillator import DampedOscillator
from forcing import SinusoidalForcing

class SpectralAnalyzer:
    def __init__(self, t: np.ndarray, x: np.ndarray):
        """Initializes the analyzer and validates uniform sampling."""
        if len(t) < 2:
            raise ValueError("Time array must contain at least 2 samples.")
        
        # Verify uniform sampling
        dt_array = np.diff(t)
        self.dt = dt_array[0]
        if not np.allclose(dt_array, self.dt, atol=1e-6):
            raise ValueError("FFT requires uniformly sampled data. Non-uniform time grid detected.")
            
        self.t = t
        self.x = x
        self.N = len(x)
        self.fs = 1.0 / self.dt
        self.nyquist = self.fs / 2.0
        self.df = self.fs / self.N
        self.duration = t[-1] - t[0]

    def remove_transient(self, cutoff_time: float):
        """Removes the early transient portion of the signal."""
        if cutoff_time >= self.t[-1]:
            raise ValueError("Cutoff time exceeds simulation duration.")
        idx = np.searchsorted(self.t, cutoff_time)
        self.t = self.t[idx:]
        self.x = self.x[idx:]
        self.N = len(self.x)
        self.df = self.fs / self.N
        self.duration = self.t[-1] - self.t[0]

    def compute_fft(self, window: str = 'boxcar', pad_factor: int = 1) -> Dict[str, np.ndarray]:
        """
        Computes the one-sided FFT with optional windowing and zero padding.
        Applies coherent gain normalization for windows.
        """
        if pad_factor < 1:
            raise ValueError("Zero-padding factor must be >= 1.")

        # Apply Window
        win_array = get_window(window, self.N)
        coherent_gain = np.mean(win_array)
        x_win = self.x * win_array / coherent_gain  # Normalize amplitude preservation

        # Zero Padding
        N_pad = self.N * pad_factor
        
        # Compute One-Sided FFT
        fft_complex = np.fft.rfft(x_win, n=N_pad)
        freqs = np.fft.rfftfreq(N_pad, d=self.dt)
        
        # Amplitude Normalization (2/N for one-sided, except DC/Nyquist)
        amplitude = (2.0 / self.N) * np.abs(fft_complex)
        amplitude[0] /= 2.0  # DC component
        if N_pad % 2 == 0:
            amplitude[-1] /= 2.0  # Nyquist component
            
        # Power Spectrum (Proportional to Amplitude squared)
        power = amplitude**2
        
        # Phase Extraction
        phase_rad = np.angle(fft_complex)

        return {
            'frequency_hz': freqs,
            'angular_frequency': 2 * np.pi * freqs,
            'fft_complex': fft_complex,
            'amplitude': amplitude,
            'power': power,
            'phase_rad': phase_rad,
            'window': window,
            'pad_factor': pad_factor
        }

    def detect_dominant_frequency(self, fft_data: Dict[str, np.ndarray]) -> Dict[str, float]:
        """Identifies the peak spectral component."""
        freqs = fft_data['frequency_hz']
        amps = fft_data['amplitude']
        
        max_idx = np.argmax(amps)
        return {
            'dominant_frequency_hz': freqs[max_idx],
            'dominant_angular_freq': fft_data['angular_frequency'][max_idx],
            'peak_amplitude': amps[max_idx],
            'peak_phase_rad': fft_data['phase_rad'][max_idx],
            'peak_power': fft_data['power'][max_idx]
        }

    def compute_welch_psd(self, nperseg: int = 256, window: str = 'hann') -> Dict[str, np.ndarray]:
        """Calculates the Power Spectral Density using Welch's method."""
        freqs, psd = welch(self.x, fs=self.fs, window=window, nperseg=nperseg)
        return {
            'frequency_hz': freqs,
            'angular_frequency': 2 * np.pi * freqs,
            'psd': psd
        }

# --- Demonstration & Visualization Functions ---

def demo_aliasing():
    """Demonstrates Nyquist limits and Aliasing."""
    f_signal = 12.0  # True frequency
    fs_good = 50.0   # Well above Nyquist (24 Hz)
    fs_bad = 15.0    # Below Nyquist -> Aliasing occurs
    
    t_good = np.arange(0, 2.0, 1.0/fs_good)
    t_bad = np.arange(0, 2.0, 1.0/fs_bad)
    
    x_good = np.cos(2 * np.pi * f_signal * t_good)
    x_bad = np.cos(2 * np.pi * f_signal * t_bad)
    
    fft_good = SpectralAnalyzer(t_good, x_good).compute_fft()
    fft_bad = SpectralAnalyzer(t_bad, x_bad).compute_fft()
    
    # Expected aliased frequency: |f_signal - N * fs|
    f_aliased = abs(f_signal - fs_bad) # 15 - 12 = 3 Hz
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle(f"Aliasing Demonstration (True Signal = {f_signal} Hz)")
    
    axs[0].plot(fft_good['frequency_hz'], fft_good['amplitude'], 'b.-', label=f'Properly Sampled ($f_s={fs_good}$ Hz)')
    axs[0].axvline(f_signal, color='k', linestyle='--', label='True Frequency')
    axs[0].set_title(f"Nyquist Limit Respected ($f_{{Nyquist}} = {fs_good/2}$ Hz)")
    axs[0].legend(); axs[0].grid(True)
    
    axs[1].plot(fft_bad['frequency_hz'], fft_bad['amplitude'], 'r.-', label=f'Undersampled ($f_s={fs_bad}$ Hz)')
    axs[1].axvline(f_aliased, color='k', linestyle='--', label=f'Aliased Frequency ({f_aliased} Hz)')
    axs[1].set_title(f"Aliasing Occurs ($f_{{Nyquist}} = {fs_bad/2}$ Hz)")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].legend(); axs[1].grid(True)
    plt.tight_layout()
    plt.show()

def demo_windows_and_leakage():
    """Compares different windows and their effect on spectral leakage."""
    # Create a signal that does not fall perfectly on a frequency bin
    t = np.linspace(0, 10, 1000, endpoint=False)
    f_signal = 1.345
    x = np.cos(2 * np.pi * f_signal * t)
    
    analyzer = SpectralAnalyzer(t, x)
    windows = ['boxcar', 'hann', 'hamming', 'blackman']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for win in windows:
        fft_data = analyzer.compute_fft(window=win, pad_factor=4)
        ax.plot(fft_data['frequency_hz'], fft_data['amplitude'], label=win.capitalize())
        
    ax.set_xlim(1.0, 1.7)
    ax.set_title(f"Spectral Leakage & Window Comparison (Signal at {f_signal} Hz)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.legend(); ax.grid(True)
    plt.tight_layout()
    plt.show()

def run_forced_fft_analysis():
    """Runs a full FFT on a forced damped oscillator to extract steady-state response."""
    m, b, k = 1.0, 0.5, 10.0
    f_drive_hz = 0.5
    omega_drive = 2 * np.pi * f_drive_hz
    F0 = 2.0
    
    forcing = SinusoidalForcing(F0, omega_drive)
    osc = DampedOscillator(m, b, k, duration=40, num_samples=4000, forcing_function=forcing)
    res = osc.simulate(rtol=1e-7, atol=1e-7)
    
    analyzer = SpectralAnalyzer(res['time'], res['displacement'])
    
    # Analyze full signal vs steady state
    fft_full = analyzer.compute_fft()
    
    analyzer.remove_transient(cutoff_time=20.0)
    fft_steady = analyzer.compute_fft(window='hann', pad_factor=4)
    dom = analyzer.detect_dominant_frequency(fft_steady)
    
    print("\n--- FFT Forced Oscillator Analysis ---")
    print(f"Sampling Frequency:  {analyzer.fs:.2f} Hz")
    print(f"Nyquist Limit:       {analyzer.nyquist:.2f} Hz")
    print(f"Frequency Res (df):  {analyzer.df:.4f} Hz")
    print(f"Driving Freq:        {f_drive_hz:.4f} Hz")
    print(f"Detected Freq (FFT): {dom['dominant_frequency_hz']:.4f} Hz")
    print(f"Frequency Error:     {abs(f_drive_hz - dom['dominant_frequency_hz']):.2e} Hz")
    
    # Export and Plot
    export_spectral_data(fft_steady, dom)
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    axs[0].plot(res['time'], res['displacement'], 'k-', alpha=0.5, label='Full Signal')
    axs[0].plot(analyzer.t, analyzer.x, 'r-', label='Steady-State Analyzed Portion')
    axs[0].set_title("Time-Domain Displacement (Transient Removal)")
    axs[0].legend(); axs[0].grid(True)
    
    axs[1].plot(fft_steady['frequency_hz'], fft_steady['amplitude'], 'b-')
    axs[1].axvline(f_drive_hz, color='k', linestyle='--', label=f'Driving Freq ({f_drive_hz} Hz)')
    axs[1].set_xlim(0, 1.5)
    axs[1].set_title("Steady-State FFT Amplitude Spectrum")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("Amplitude")
    axs[1].legend(); axs[1].grid(True)
    plt.tight_layout()
    plt.show()

def export_spectral_data(fft_data: Dict, dom: Dict):
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results', 'spectral'), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'spectral', 'fft_displacement.csv')
    
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['frequency_hz', 'angular_frequency', 'amplitude', 'power', 'phase_rad'])
        for i in range(len(fft_data['frequency_hz'])):
            writer.writerow([
                fft_data['frequency_hz'][i], fft_data['angular_frequency'][i],
                fft_data['amplitude'][i], fft_data['power'][i], fft_data['phase_rad'][i]
            ])

if __name__ == "__main__":
    print("Running Aliasing Demonstration...")
    demo_aliasing()
    print("Running Window Leakage Demonstration...")
    demo_windows_and_leakage()
    print("Running Forced FFT Analysis...")
    run_forced_fft_analysis()
