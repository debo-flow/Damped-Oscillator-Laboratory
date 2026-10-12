# Performance and Scientific Validation

This document outlines the numerical rigor applied to the Damped Oscillator Laboratory.

## Solver Selection & Stiffness
While standard explicit methods (`RK45`, `DOP853`) are highly efficient for linear, coupled, and mildly nonlinear systems (like Duffing), they can fail catastrophically on *stiff* equations. The Van der Pol oscillator at large $\mu \gg 1$ exhibits relaxation oscillations with immense velocity spikes. The `NumericalBackend` advises routing these topologies to implicit solvers like `Radau` or `BDF`, which evaluate Jacobians to maintain stability without forcing time-steps to shrink toward zero.

## Cross-Solver Validation
Agreement between different families of solvers (e.g., Runge-Kutta vs. Backward Differentiation Formula) serves as foundational evidence that observed chaotic behaviors are genuine physical properties of the continuous ODE, rather than discrete integration artifacts.

## Energy Balance Validation
For conservative ($c=0$) systems, the Hamiltonian $E(t) = \frac{1}{2}mv^2 + \frac{1}{2}kx^2$ is strictly constant. For dissipative systems, we validate the trajectory by integrating the power dissipated:
$$E(t) - E(0) = \int_0^t -c v(\tau)^2 d\tau$$
Residuals approaching numerical zero indicate high trajectory fidelity.
