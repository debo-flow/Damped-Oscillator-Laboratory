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
*   **Displacement Error:** $e_x(t) = |x_{numerical}(t) - x_{analytical}(t)|$
*   **Velocity Error:** $e_v(t) = |v_{numerical}(t) - v_{analytical}(t)|$

Reducing the relative tolerance (`rtol`) in the Runge-Kutta 45 integration systematically reduces the Root Mean Square (RMS) error toward zero.

## 5. Phase-Space Dynamics & State-Space Formulation
To analyze the system geometrically, we transition to **State-Space Formulation**. We define two state variables based on displacement and velocity:
*   $x_1 = x$
*   $x_2 = v = \dot{x}$

This transforms our second-order equation into a system of two first-order equations:
1.  $\dot{x} = v$
2.  $\dot{v} = -\frac{b}{m}v - \frac{k}{m}x$

### Phase Portraits and Equilibrium
By plotting displacement ($x$) on the horizontal axis and velocity ($v$) on the vertical axis, we create a **Phase Portrait**. 
The unforced damped oscillator has a single **equilibrium point** at $(x,v) = (0,0)$. Because energy is strictly decreasing due to damping, all trajectories will ultimately converge to this exact point, representing the system coming to a complete rest.

*   **Underdamped:** Trajectories spiral inward toward $(0,0)$.
*   **Critically / Overdamped:** Trajectories approach $(0,0)$ without spiraling.

### Energy Contours vs. Dissipative Trajectories
For an *undamped* oscillator, the total mechanical energy is conserved:
$$E = \frac{1}{2}mv^2 + \frac{1}{2}kx^2 = \text{Constant}$$
In phase space, these constant energies form closed ellipses (energy contours). However, for a *damped* system, the trajectory slices inward across these contours, visually demonstrating the continuous dissipation of energy over time.

### Dimensionless Phase Space
To compare systems with wildly different mass/spring values, we normalize the axes:
*   **Dimensionless Displacement:** $X = \frac{x}{x_{scale}}$
*   **Dimensionless Velocity:** $V = \frac{v}{x_{scale} \cdot \omega_0}$
## 6. Energy Dynamics and Dissipation
The total mechanical energy $E$ of the system is the sum of Kinetic Energy ($K$) and Potential Energy ($U$):
*   **Kinetic Energy:** $K = \frac{1}{2}mv^2$
*   **Potential Energy:** $U = \frac{1}{2}kx^2$
*   **Total Mechanical Energy:** $E(t) = K(t) + U(t)$

### Power and the Damping Force
The internal forces dictating the system are the restoring spring force ($F_s = -kx$) and the damping force ($F_d = -bv$). Because the damping force resists motion, it does negative work, extracting energy from the system. The instantaneous damping power is:
$$P_d = F_d v = -bv^2$$

Consequently, the theoretical time-derivative of the mechanical energy is entirely governed by this dissipation:
$$\frac{dE}{dt} = -bv^2$$

### The Energy Balance Equation
By integrating the damping power over time, we calculate the total energy lost as heat ($E_{diss}$). The energy balance of the system mandates that the current mechanical energy must equal the initial energy minus the dissipated energy:
$$E(t) = E(0) - \int_0^t bv^2(\tau)d\tau$$

In a numerically perfect simulation, the residual equation $R_E(t) = E(0) - E(t) - E_{diss}(t)$ will evaluate exactly to zero. Tracking $R_E(t)$ serves as a rigorous convergence metric for the underlying ODE solver.
