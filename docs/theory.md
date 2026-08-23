# Theory: Damped Harmonic Oscillator

## 1. Simple Harmonic Motion & Damping
A simple harmonic oscillator has a restoring force proportional to displacement ($F = -kx$). Damping introduces a drag force proportional to velocity ($F_d = -b\dot{x}$). The combination yields the fundamental equation of motion:

$$m\ddot{x} + b\dot{x} + kx = 0$$

## 2. Natural Parameters & The Characteristic Equation
By defining the **Natural Angular Frequency** ($\omega_0 = \sqrt{\frac{k}{m}}$) and the **Damping Ratio** ($\zeta = \frac{b}{2\sqrt{mk}}$), the equation can be rewritten as:

$$\ddot{x} + 2\zeta\omega_0\dot{x} + \omega_0^2x = 0$$

Assuming solutions of the form $x(t) = e^{rt}$, we get the characteristic equation: $r^2 + 2\zeta\omega_0r + \omega_0^2 = 0$. The nature of its roots determines the system's behavior based on the discriminant ($\Delta = b^2 - 4mk$).

## 3. Damping Regimes and Analytical Solutions

### Underdamped ($0 \le \zeta < 1$ or $\Delta < 0$)
The roots are complex conjugates. The system oscillates, but the amplitude decays exponentially.
*   **Damped Angular Frequency:** $\omega_d = \omega_0\sqrt{1 - \zeta^2}$
*   **Analytical Solution:** $x(t) = A e^{-\zeta\omega_0 t} \cos(\omega_d t + \phi)$

### Critically Damped ($\zeta = 1$ or $\Delta = 0$)
The roots are real and identical. The system returns to equilibrium as fast as possible without oscillating.
*   **Analytical Solution:** $x(t) = (A + Bt) e^{-\omega_0 t}$

### Overdamped ($\zeta > 1$ or $\Delta > 0$)
The roots ($r_1, r_2$) are real and distinct. The system experiences high resistance and slowly creeps back to equilibrium without oscillating.
*   **Analytical Solution:** $x(t) = A e^{r_1 t} + B e^{r_2 t}$
*   **Roots:** $r_{1,2} = \frac{-b \pm \sqrt{b^2 - 4mk}}{2m}$

## 4. Analytical Velocity & Error Analysis
Because velocity dictates kinetic energy and damping force, numerical differentiation introduces lag. We calculate velocity analytically natively using $v(t) = \frac{dx}{dt}$. 

Numerical approximation fidelity is quantified via Absolute Error equations:
*   **Displacement Error:** $e_x(t) = \vert{}x_{numerical}(t) - x_{analytical}(t)\vert{}$
*   **Velocity Error:** $e_v(t) = \vert{}v_{numerical}(t) - v_{analytical}(t)\vert{}$

Reducing the relative tolerance (`rtol`) in the Runge-Kutta 45 integration systematically reduces the Root Mean Square (RMS) error toward zero.
