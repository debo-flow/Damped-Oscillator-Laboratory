# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped harmonic oscillators. The engine solves classical equations of motion using numerical integration, calculates kinetic/potential energy, compares findings against analytical solutions, and visualizes the system's geometric evolution through detailed phase-space analysis.

## Physics Equation
The core physics engine solves:
$$m\ddot{x} + b\dot{x} + kx = 0$$

Transformed into state-space representation for phase analysis:
* $\dot{x} = v$
* $\dot{v} = -\frac{b}{m}v - \frac{k}{m}x$

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp`.
*   **Analytical Engine:** Exact mathematical solutions modeled for displacement and velocity.
*   **Validation Lab:** Root Mean Square (RMS) error tracking and solver convergence studies.
*   **Phase-Space Laboratory:** Deep geometric analysis featuring $x-v$ phase portraits, stream-plot vector fields, energy contour overlays, dimensionless plotting, and multi-IC trajectory comparisons.
*   **Automated Testing:** `pytest` regression suite ensuring numerical stability and strict mathematical accuracy.

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
│   └── phase_space.py
├── tests/
│   ├── test_validation.py
│   └── test_phase_space.py
├── docs/
│   └── theory.md
└── results/
    └── validation/
