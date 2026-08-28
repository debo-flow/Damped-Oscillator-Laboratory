## 7. Forced Damped Oscillations
If an external periodic force acts upon the system, the equation of motion becomes non-homogeneous:
$$m\ddot{x} + b\dot{x} + kx = F_0\cos(\omega t)$$
Where $F_0$ is the driving amplitude and $\omega$ is the driving angular frequency.

### Transient and Steady-State Response
By the principle of superposition, the total analytical solution is the sum of two components:
1.  **Transient Response ($x_{transient}$):** The general solution to the unforced homogeneous equation. It depends on initial conditions and decays exponentially due to damping.
2.  **Steady-State Response ($x_{steady}$):** The particular solution representing the long-term periodic behavior forced by the external drive.

The steady-state displacement is given by $x_{steady}(t) = X(\omega)\cos(\omega t - \phi)$, where:
*   **Amplitude:** $X(\omega) = \frac{F_0}{\sqrt{(k - m\omega^2)^2 + (b\omega)^2}}$
*   **Phase Lag:** $\phi = \operatorname{atan2}(b\omega, k - m\omega^2)$

### Forced Phase-Space and Energy
Unlike the unforced oscillator where the trajectory spirals to a $(0,0)$ equilibrium, the forced oscillator eventually settles into a closed, periodic elliptical orbit in phase space (a **Limit Cycle**), independent of the initial starting conditions. 
In this steady state, the net energy is balanced: the average mechanical power injected by the driving force ($P_{drive} = F_{drive}v$) exactly matches the average heat dissipated by the damping force ($P_d = -bv^2$).
