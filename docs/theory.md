## 17. Global Phase-Space Structure and Invariant Manifolds
While local linearization provides eigenvectors at an equilibrium, global dynamics are governed by **Invariant Manifolds**—nonlinear curves (or surfaces) that trajectories follow as they approach or flee fixed points over infinite time.

### Stable and Unstable Manifolds ($W^s$, $W^u$)
For a hyperbolic equilibrium point $\mathbf{x}^*$:
*   **Stable Manifold ($W^s$):** The set of all initial conditions that asymptotically converge to $\mathbf{x}^*$ as $t \to +\infty$. Numerically, this is approximated by integrating the local stable eigenvector ($E^s$) *backward* in time.
*   **Unstable Manifold ($W^u$):** The set of all initial conditions that converge to $\mathbf{x}^*$ as $t \to -\infty$. Numerically, this is approximated by integrating the local unstable eigenvector ($E^u$) *forward* in time.

### Separatrices and Basin Boundaries
In bistable systems like the Double-Well Duffing oscillator, the Stable Manifold of the central saddle point acts as a **Separatrix**—a geometric boundary separating the basins of attraction of the two stable wells. Trajectories on opposite sides of $W^s$ will ultimately fall into entirely different attractors.

### Homoclinic and Heteroclinic Connections
*   **Homoclinic Orbit:** A trajectory that lies in both $W^u(\mathbf{x}^*)$ and $W^s(\mathbf{x}^*)$. The trajectory leaves the saddle and eventually returns to the exact same saddle, taking infinite time.
*   **Heteroclinic Orbit:** A trajectory that connects two different saddle points ($W^u(\mathbf{x}_A^*) \cap W^s(\mathbf{x}_B^*)$).
*Note: Due to numerical precision, we classify these as "candidates." Rigorous mathematical proof of a true intersection often requires topological methods like Melnikov integrals.*
