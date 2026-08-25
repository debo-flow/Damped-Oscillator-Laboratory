# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped harmonic oscillators. The engine solves classical equations of motion using numerical integration, evaluates state-space geometric formulations, and tracks the exact thermodynamic dissipation of mechanical energy over time to prove conservation equations.

## Physics Equation
The core physics engine solves:
$$m\ddot{x} + b\dot{x} + kx = 0$$

Governed by the instantaneous energy balance equation:
$$E(t) = E(0) - \int_0^t bv^2(\tau)d\tau$$

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp`.
*   **Validation Lab:** Root Mean Square (RMS) error tracking and solver convergence studies.
*   **Phase-Space Laboratory:** Deep geometric analysis featuring $x-v$ phase portraits, stream-plot vector fields, and multi-IC trajectory comparisons.
*   **Energy Dynamics Laboratory:** Quantitative verification of mechanical energy transformation, isolating $K$, $U$, $E$, instantaneous damping power ($P_d = -bv^2$), and rigorous numerical integration of dissipated heat.
*   **Data Export:** Automated export of solver accuracy and thermodynamic data matrices to CSV files.
*   **Automated Testing:** `pytest` regression suite ensuring numerical stability, undamped $b=0$ conservation limits, and mathematical accuracy.

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
│   └── energy_analysis.py
├── tests/
│   ├── test_validation.py
│   ├── test_phase_space.py
│   └── test_energy_analysis.py
├── docs/
│   └── theory.md
└── results/
    ├── validation/
    └── energy/
