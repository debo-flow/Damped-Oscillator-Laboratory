# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped harmonic oscillators. The engine solves classical equations of motion using numerical integration, calculates kinetic/potential energy, and compares findings against analytical solutions across various damping regimes.

## Physics Equation
The core physics engine solves:
$$m\ddot{x} + b\dot{x} + kx = 0$$

Using the damping ratio $\zeta = \frac{b}{2\sqrt{mk}}$, the laboratory classifies the system into three regimes:
*   $\zeta < 1$: Underdamped
*   $\zeta = 1$: Critically Damped
*   $\zeta > 1$: Overdamped

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp`.
*   **Damping Analysis:** Automated classification of natural frequencies, discriminant, and damping ratio.
*   **Analytical Engine:** Exact mathematical solutions modeled for absolute error comparisons.
*   **Visualization Suite:** Extensive Matplotlib plotting for displacements, velocities, mechanical energies, and numerical-vs-analytical accuracy tests.

## Project Structure
```text
Damped-Oscillator-Laboratory/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── damped_oscillator.py   # Core physics engine and analytical formulas
│   └── damping_analysis.py    # Multi-regime simulation and comparison
├── docs/
│   └── theory.md
└── results/
    └── .gitkeep
