# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped, driven, and coupled harmonic oscillators. The engine bridges time-domain integration with advanced frequency-domain spectral analysis, analyzing thermodynamic energy balancing, geometric limit cycles, and generalized eigenvalue normal-mode phenomena.

## Physics Equation
The core physics engine solves scalar non-homogeneous ODEs as well as N-Degree-of-Freedom matrix coupled formulations:
$$\mathbf{M}\ddot{\mathbf{x}} + \mathbf{C}\dot{\mathbf{x}} + \mathbf{K}\mathbf{x} = \mathbf{0}$$

Which is analyzed for discrete normal modes via generalized eigen-decomposition:
$$\mathbf{K}\mathbf{u} = \omega^2 \mathbf{M}\mathbf{u}$$

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp` supporting singular and multi-mass coupled systems.
*   **Normal Modes Laboratory:** Extracts generalized eigenvalues/eigenvectors to map Symmetric and Antisymmetric mode shapes, normal frequencies ($\omega_i$), and modal superpositions.
*   **Coupled Phase-Space & Energy:** Tracks complete energy exchange/beating phenomena between subsystems ($E_{osc1} \rightleftharpoons E_{osc2}$) while preserving global mechanical energy tracking.
*   **Spectral Analysis Lab:** Fast Fourier Transform (FFT) analysis, windowing, PSD, and aliasing demonstrations to detect frequency components in multi-mode states.
*   **Frequency Response Lab:** Theoretical Bode sweeps verifying resonant frequencies ($\omega_r$) and Quality Factors ($Q$).
*   **Automated Testing:** `pytest` regression suite mathematically guaranteeing matrix constructions, energy conservation, uncoupled equivalents ($k_c=0$), and FFT peak alignments.

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
│   ├── spectral_analysis.py
│   └── coupled_oscillators.py
├── tests/
│   ├── test_validation.py
│   ├── test_phase_space.py
│   ├── test_energy_analysis.py
│   ├── test_forced_oscillator.py
│   ├── test_resonance.py
│   ├── test_spectral_analysis.py
│   └── test_coupled_oscillators.py
├── docs/
│   └── theory.md
└── results/
