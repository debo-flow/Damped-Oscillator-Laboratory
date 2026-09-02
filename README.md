# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment studying the physics of linear, nonlinear, and coupled harmonic oscillators. The engine explores thermodynamic balancing, generalized normal modes, and computational chaos theory, utilizing advanced discrete stroboscopic diagnostics.

## Physics Equation
The core physics engine supports forced double-well Duffing potentials commonly used to model chaotic dynamics:
$$m\ddot{x} + b\dot{x} + kx + \alpha x^3 = F_0\cos(\omega t)$$

## Features
*   **Chaos Diagnostics Lab:** Implements exact stroboscopic interpolations to map continuous phase-space trajectories into discrete Poincaré Sections.
*   **Bifurcation & Parameter Sweeps:** Executes continuous parameter sweeps mapping steady-state Poincaré points to visualize period-doubling cascades and transitions into complexity.
*   **Periodicity Clustering:** Automatically analyzes point clouds to detect stable $N$-period limit cycles versus complex non-repeating strange attractors.
*   **Sensitive Dependence:** Runs tightly paired parallel simulations to dynamically plot $d(t)$ trajectory separation (the butterfly effect).
*   **Recurrence & Transients:** Provides binary recurrence matrices and precise transient-removal systems to isolate true long-term asymptotic behavior.
*   **Experiment Presets:** Includes reproducible JSON experiment files isolating specific period-1, period-2, and complex Duffing regimes.

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
│   └── chaos_analysis.py
├── experiments/
│   ├── periodic_case.json
│   ├── period_doubling_case.json
│   ├── complex_case.json
│   └── solver_sensitivity_case.json
├── tests/
│   ├── test_chaos_analysis.py
│   └── (all previous tests...)
├── docs/
│   └── theory.md
└── results/
