## 11. Nonlinear Oscillators and Duffing Dynamics
When the restoring force of a spring is no longer strictly proportional to displacement (Hooke's Law), the system becomes nonlinear. The canonical model is the **Duffing Oscillator**, which introduces a cubic nonlinearity $\alpha x^3$:

$$m\ddot{x} + b\dot{x} + kx + \alpha x^3 = F(t)$$

### Nonlinear Restoring Force and Potential Energy
The total restoring force is $F_{spring}(x) = -kx - \alpha x^3$. Integrating this with respect to displacement gives the nonlinear potential energy:
$$U(x) = \frac{1}{2}kx^2 + \frac{1}{4}\alpha x^4$$
Therefore, the total mechanical energy is $E = \frac{1}{2}mv^2 + \frac{1}{2}kx^2 + \frac{1}{4}\alpha x^4$.

### Hardening vs. Softening Regimes
*   **Hardening Spring ($\alpha > 0$):** The effective stiffness increases as amplitude grows. The potential energy forms a steep "well". Oscillation frequency generally *increases* with amplitude, and resonance response curves bend toward higher frequencies.
*   **Softening Spring ($\alpha < 0$):** The effective stiffness decreases as amplitude grows. At large displacements, the $x^4$ term dominates negatively, making the potential energy unbounded below. Global stability is lost, but stable bounded orbits can exist for small energies. The resonance curve bends toward lower frequencies.

### Multistability, Hysteresis, and Harmonics
Unlike linear systems, forced nonlinear oscillators can exhibit **multistability**—multiple stable steady-state amplitudes for the exact same driving frequency.
Depending on the initial conditions (or the direction of a frequency sweep), the system may follow different response branches, occasionally exhibiting sudden **jumps** between them (hysteresis). Furthermore, a purely sinusoidal input will generate a response containing higher-order **harmonics** (e.g., $3\omega$, $5\omega$) due to the cubic distortion.
