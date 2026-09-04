# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment studying the physics of linear, nonlinear, and coupled harmonic oscillators. The engine bridges discrete stroboscopic diagnostics with advanced continuous-time quantitative chaos theory, computing comprehensive Lyapunov spectrums and fractal attractor topologies.

## Features
*   **Full Lyapunov Spectrum Lab:** Integrates complete phase-space Tangent Dynamics ($\dot{V} = J(\mathbf{x}, t) V$) paired with numerical QR-Decomposition reorthonormalization to flawlessly extract ordered Lyapunov spectrums ($\lambda_1 \dots \lambda_n$).
*   **Fractal Dimension Diagnostics:** Implements numerical scaling-region algorithms to compute topological complexities including Box-Counting ($D_{box}$), Correlation Dimension ($D_2$), and the spectrum-derived Kaplan-Yorke Dimension ($D_{KY}$).
*   **Attractor Geometry Tracking:** Generates bounded limits, centroid RMS metrics, and memory-safe pairwise distance correlation matrices for steady-state post-transient complex attractors.
*   **Automated Testing:** `pytest` regression suite ensuring absolute analytical boundaries. Tests QR-orthogonality limits ($\vert{}Q^TQ - I\vert{} < 10^{-10}$), Kaplan-Yorke index edge cases, and memory OOM safeguards for massive datasets.

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
│   ├── coupled_oscillators.py
│   ├── nonlinear_oscillators.py
│   ├── van_der_pol.py
│   ├── chaos_analysis.py
│   ├── lyapunov_analysis.py
│   └── attractor_analysis.py
├── experiments/
│   ├── periodic_case.json
│   ├── complex_case.json
│   ├── lyapunov_validation.json
│   ├── lyapunov_scan.json
│   └── attractor_dimension.json
├── tests/
│   ├── test_lyapunov_analysis.py
│   ├── test_attractor_analysis.py
│   └── (all previous tests...)
├── docs/
│   └── theory.md
└── results/
