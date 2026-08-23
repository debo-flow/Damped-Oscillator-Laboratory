# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped harmonic oscillators. The engine solves classical equations of motion using numerical integration, calculates kinetic/potential energy, and compares findings against analytical solutions across various damping regimes to conduct rigorous error and convergence analysis.

## Physics Equation
The core physics engine solves:
$$m\ddot{x} + b\dot{x} + kx = 0$$

Using the damping ratio $\zeta = \frac{b}{2\sqrt{mk}}$, the laboratory classifies the system into three regimes:
*   $\zeta < 1$: Underdamped
*   $\zeta = 1$: Critically Damped
*   $\zeta > 1$: Overdamped

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp` with configurable tolerances.
*   **Damping Analysis:** Automated classification of natural frequencies, discriminant, and damping ratio.
*   **Analytical Engine:** Exact mathematical solutions modeled for displacement and velocity.
*   **Validation Lab:** Root Mean Square (RMS) error tracking, solver convergence studies, and automated regression testing.
*   **Visualization Suite:** Extensive Matplotlib plotting for displacements, velocities, mechanical energies, and absolute error comparisons.

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
│   └── validation_lab.py
├── tests/
│   └── test_validation.py
├── docs/
│   └── theory.md
└── results/
    └── validation/
