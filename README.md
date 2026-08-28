# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped and driven harmonic oscillators. The engine solves classical equations of motion using numerical integration, evaluates state-space geometric limit cycles, tracks precise thermodynamic power inputs, and performs exact frequency-domain resonance analysis.

## Physics Equation
The core physics engine solves the non-homogeneous ODE:
$$m\ddot{x} + b\dot{x} + kx = F_0\cos(\omega t)$$

Steady-State Resonance Amplitude Equation:
$$X(\omega) = \frac{F_0}{\sqrt{(k - m\omega^2)^2 + (b\omega)^2}}$$

## Features
*   **Physics Engine:** Numerical simulation using `scipy.integrate.solve_ivp` with a modular external forcing interface.
*   **Frequency Response Lab:** Theoretical Bode-style plots mapping Amplitude $X(\omega)$ and Phase Lag $\phi(\omega)$ across configurable logarithmic and linear frequency sweeps.
*   **Resonance & Q-Factor Tracking:** Automated numerical refinement of resonance frequencies ($\omega_r$), half-power bandwidth limits ($\Delta\omega$), and Quality Factors ($Q$).
*   **Time-Domain Validation:** Direct steady-state thermodynamic balancing proving $\langle P_{drive} \rangle = -\langle P_{damping} \rangle$ at resonance points.
*   **Phase-Space Laboratory:** $x-v$ phase portraits capturing initial condition convergence onto steady-state limit cycles.
*   **Data Export:** Automated export of solver accuracy, thermodynamic matrices, and frequency-response sweeps to CSV files.
*   **Automated Testing:** `pytest` regression suite ensuring numerical stability, strict mathematical superposition, and bounds testing for non-resonant heavy damping scenarios.

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
│   ├── forced_analysis.py
│   └── resonance_analysis.py
├── tests/
│   ├── test_validation.py
│   ├── test_phase_space.py
│   ├── test_energy_analysis.py
│   ├── test_forced_oscillator.py
│   └── test_resonance.py
├── docs/
│   └── theory.md
└── results/
