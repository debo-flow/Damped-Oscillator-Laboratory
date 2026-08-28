## 8. Resonance and Frequency Response
When the damped oscillator is driven by a periodic force $F_0\cos(\omega t)$, the steady-state displacement depends heavily on the driving angular frequency $\omega$.

### Amplitude and Phase Response
The theoretical steady-state amplitude $X(\omega)$ and phase lag $\phi(\omega)$ are given by:
$$X(\omega) = \frac{F_0}{\sqrt{(k - m\omega^2)^2 + (b\omega)^2}}$$
$$\phi(\omega) = \text{atan2}(b\omega, k - m\omega^2)$$

*   **Low Frequency Limit:** As $\omega \to 0$, the system acts quasi-statically, yielding $X(0) \approx F_0 / k$.
*   **High Frequency Limit:** As $\omega \to \infty$, inertia dominates, and the displacement amplitude approaches zero.

### Resonance Frequency
If the damping ratio is sufficiently small ($\zeta < \frac{1}{\sqrt{2}} \approx 0.707$), the amplitude-frequency response exhibits a distinct peak. The frequency at which this maximum occurs is the **Resonance Frequency** ($\omega_r$):
$$\omega_r = \omega_0\sqrt{1 - 2\zeta^2}$$
Note that $\omega_r$ is always slightly lower than the natural frequency ($\omega_0$). For strongly damped systems ($\zeta \ge \frac{1}{\sqrt{2}}$), no interior amplitude peak exists, and the maximum displacement strictly occurs at $\omega = 0$.

### Bandwidth and Quality Factor
The **Half-Power Frequencies** ($\omega_1, \omega_2$) occur where the amplitude drops to $X_{max} / \sqrt{2}$ (which corresponds to half the maximum power). The **Bandwidth** is the distance between them ($\Delta\omega = \omega_2 - \omega_1$). 
The **Quality Factor** ($Q$) measures the sharpness of the resonance peak:
$$Q = \frac{\omega_r}{\Delta\omega}$$
For a lightly damped linear oscillator, the theoretical quality factor can be calculated directly as $Q = \frac{m\omega_0}{b}$.

### Steady-State Energy Balance
At resonance, the average mechanical power injected into the system by the driving force exactly equals the average power dissipated by the damping mechanism:
$$\langle P_{drive} \rangle \approx -\langle P_{damping} \rangle$$
