# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment studying the physics of linear, nonlinear, and coupled harmonic oscillators. The engine bridges discrete stroboscopic diagnostics with advanced continuous-time quantitative chaos theory to calculate definitive mathematical classifications.

## Physics Equation
The Lyapunov analysis framework features a generic interface supporting analytical stability evaluations and highly nonlinear non-autonomous chaotic states, including the Duffing potential:
$$m\ddot{x} + b\dot{x} + kx + \alpha x^3 = F_0\cos(\omega t)$$

## Features
*   **Quantitative Chaos Lab:** Implements the continuous Benettin Renormalization algorithm to calculate Finite-Time Largest Lyapunov Exponents ($\lambda_{max}$).
*   **Convergence Diagnostics:** Generates cumulative log-growth graphs tracing local Lyapunov fluctuations as they asymptotically converge onto their true physical value.
*   **Jacobian Integrations:** Provides automated, finite-difference Jacobian approximations ($J = \partial f / \partial \mathbf{x}$) laying the foundation for full Lyapunov Spectrum extraction.
*   **Parameter Bifurcation Maps:** Automates 1D Parameter scans, plotting $\lambda_{max}$ versus varying forcing amplitudes ($F_0$) to exactly pinpoint critical bifurcation phase boundaries (where $\lambda$ crosses 0).
*   **Discrete Chaos Diagnostics:** Implements stroboscopic interpolations mapping continuous trajectories into Poincaré Sections and recurrence matrices.
*   **Automated Testing:** `pytest` regression suite ensuring flawless positive control validations: guaranteeing strictly negative $\lambda_{max}$ for damped states, and $\lambda_{max} \approx 0$ for neutral harmonic cycles.

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
│   └── lyapunov_analysis.py
├── experiments/
│   ├── periodic_case.json
│   ├── complex_case.json
│   ├── lyapunov_validation.json
│   └── lyapunov_scan.json
├── tests/
│   ├── test_lyapunov_analysis.py
│   └── (all previous tests...)
├── docs/
│   └── theory.md
└── results/
