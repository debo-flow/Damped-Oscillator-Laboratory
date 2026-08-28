# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped and driven harmonic oscillators. The engine solves classical equations of motion using numerical integration, evaluates state-space geometric limit cycles, and tracks precise thermodynamic power inputs and dissipations.

## Physics Equation
The core physics engine solves the non-homogeneous ODE:
$$m\ddot{x} + b\dot{x} + kx = F_0\cos(\omega t)$$

Governed by the instantaneous energy balance equation:
$$E(t) = E(0) + \int_0^t \left( F_{drive}v - bv^2 \right) d\tau$$

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp` with a modular external forcing interface.
*   **Forced Response Analysis:** Exact mathematical modeling of superposition, isolating exponentially decaying transients from periodic steady-state limits.
*   **Validation Lab:** Root Mean Square (RMS) error tracking and automated solver convergence testing.
*   **Phase-Space Laboratory:** $x-v$ phase portraits capturing initial condition convergence onto steady-state limit cycles.
*   **Energy Dynamics Laboratory:** Quantitative verification of mechanical energy transformation, isolating $P_{drive}$ and $P_{damping}$ to prove total system energy conservation.
*   **Automated Testing:** `pytest` regression suite ensuring numerical stability, strict mathematical superposition, and unforced fallback behavior.

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
│   └── forced_analysis.py
├── tests/
│   ├── test_validation.py
│   ├── test_phase_space.py
│   ├── test_energy_analysis.py
│   └── test_forced_oscillator.py
├── docs/
│   └── theory.md
└── results/
