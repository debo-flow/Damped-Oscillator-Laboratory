# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped and driven harmonic oscillators. The engine bridges time-domain integration with advanced frequency-domain spectral analysis, analyzing thermodynamic energy balancing, geometric limit cycles, and Fourier spectral properties.

## Physics Equation
The core physics engine solves the non-homogeneous ODE:
$$m\ddot{x} + b\dot{x} + kx = F_0\cos(\omega t)$$

Which is transformed and analyzed in the spectral domain via FFT:
$$X(f) = \mathcal{F}\{x(t)\}$$

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp` with modular forcing.
*   **Spectral Analysis Lab:** Fast Fourier Transform (FFT) analysis to extract one-sided amplitude spectra, phase estimates, and Power Spectral Densities (PSD).
*   **Signal Processing Tools:** Features automated uniform-sampling validation, coherent-gain windowing (Hann, Hamming, Blackman), zero-padding for interpolation, and transient removal.
*   **Frequency Response Lab:** Theoretical Bode sweeps verifying resonant frequencies ($\omega_r$) and Quality Factors ($Q$).
*   **Phase-Space & Energy Lab:** Identifies limit cycles and validates that average mechanical input power balances average dissipated heat.
*   **Automated Testing:** `pytest` regression suite ensuring numerical stability, aliasing predictability, correct $2/N$ FFT normalization, and exact frequency recovery.

## Project Structure
```text
Damped-Oscillator-Laboratory/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── damped_oscillator.py
│   ├── damping_analysis.py
│   ├── analytical_solution.py
│   ├── validation_lab.py
│   ├── phase_space.py
│   ├── energy_analysis.py
│   ├── forcing.py
│   ├── resonance_analysis.py
│   └── spectral_analysis.py
├── tests/
│   ├── test_validation.py
│   ├── test_phase_space.py
│   ├── test_energy_analysis.py
│   ├── test_forced_oscillator.py
│   ├── test_resonance.py
│   └── test_spectral_analysis.py
├── docs/
│   └── theory.md
└── results/
