# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment to study the physics of damped harmonic oscillators. This project models mechanical vibrations subjected to damping forces, utilizing numerical integration to analyze displacement, velocity, and energy over time.

## Physics Equation
The core physics engine solves the classical equation of motion for a damped oscillator:

$$m\ddot{x} + b\dot{x} + kx = 0$$

## Features
*   **Physics Engine:** Accurate numerical simulation using `scipy.integrate.solve_ivp`.
*   **Energy Tracking:** Calculates continuous Kinetic, Potential, and Total Mechanical Energy.
*   **Visualization:** Separate, detailed Matplotlib plots for displacement, velocity, and energy decay.
*   **Validation:** Robust parameter validation to ensure physical accuracy.

## Project Structure
```text
Damped-Oscillator-Laboratory/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   └── damped_oscillator.py
├── docs/
│   └── theory.md
└── results/
    └── .gitkeep
