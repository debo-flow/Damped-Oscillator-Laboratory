## 16. Advanced Bifurcation Analysis and Continuation
Analyzing non-linear systems requires mapping how equilibria and periodic orbits change as parameters vary—a process called **Continuation**. For a system $\dot{\mathbf{x}} = f(\mathbf{x}, p)$, we seek branches of states satisfying $f(\mathbf{x}^*, p) = 0$.

### Equilibrium Stability and Local Bifurcations
Stability is determined by the continuous-time eigenvalues ($\mu_i$) of the Jacobian $J(\mathbf{x}^*, p)$:
*   **Saddle-Node Bifurcation:** Two equilibria collide and annihilate. Characterized by a purely real eigenvalue crossing zero ($Re(\mu) \to 0$, $Im(\mu) = 0$).
*   **Hopf Bifurcation:** A stable equilibrium spawns a periodic limit cycle. Characterized by a complex conjugate pair crossing the imaginary axis ($Re(\mu) \to 0$, $Im(\mu) \neq 0$).

### Periodic Orbit Stability and Floquet Theory
For periodic orbits with period $T$, stability is governed by tracking a perturbation $\delta \mathbf{x}$ over one full cycle via the **Monodromy Matrix** $M$. The eigenvalues of $M$ are called **Floquet Multipliers** ($\rho_i$). 
*   Stable orbits require all multipliers to lie strictly inside the unit circle ($\vert{}\rho_i\vert{} < 1$). (For autonomous continuous systems, one multiplier is always exactly $1$, representing perturbations along the phase of the orbit).
*   **Period-Doubling Bifurcation:** A multiplier exits the unit circle along the negative real axis ($\rho \to -1$). The orbit loses stability and spawns a new orbit with twice the period ($2T$).
*   **Neimark-Sacker (Torus) Bifurcation:** A complex conjugate pair exits the unit circle ($\vert{}\rho\vert{} \to 1$). The periodic orbit spawns a quasiperiodic Torus.

### The Feigenbaum Ratio ($\delta$)
During a period-doubling cascade leading to chaos, the parameter intervals between subsequent bifurcations shrink geometrically. The ratio of successive intervals converges to the universal Feigenbaum constant:
$$\delta_n = \frac{p_{n-1} - p_{n-2}}{p_n - p_{n-1}} \approx 4.6692$$
