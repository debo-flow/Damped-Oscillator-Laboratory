## 18. Advanced Chaos, Crisis, and Intermittency
While $\lambda_{\max} > 0$ indicates sensitive dependence, the global structure of chaos involves complex transitions and finite-time phenomena.

### Transient Chaos and Chaotic Saddles
In some regimes, trajectories behave chaotically for a long time before eventually escaping to a stable periodic orbit or infinity. This indicates the presence of a **Chaotic Saddle** (a non-attracting chaotic invariant set). The survival probability of trajectories remaining in the chaotic region typically follows an exponential decay law:
$$P(\tau > t) \approx e^{-\kappa t}$$
Where $\kappa$ is the escape rate. The finite-time Lyapunov exponent $\lambda(t)$ will remain positive during the transient phase and drop below zero upon escape.

### Intermittency
**Intermittency** occurs when a system transitions between chaos and periodic behavior. A trajectory exhibits long, nearly periodic "laminar" phases interrupted by sudden, irregular chaotic "bursts". As a control parameter $\mu$ approaches the critical bifurcation value $\mu_c$ (often a Saddle-Node), the average laminar length $\langle L \rangle$ scales according to a power law:
$$\langle L \rangle \sim |\mu - \mu_c|^{-\gamma}$$

### Crises
A **Crisis** is a sudden, discontinuous change in a chaotic attractor as a parameter varies, typically caused by the attractor colliding with an unstable periodic orbit or its stable manifold.
*   **Interior Crisis:** The chaotic attractor suddenly expands in size (e.g., variance jumps significantly).
*   **Boundary Crisis:** The chaotic attractor touches the boundary of its basin of attraction and is instantly destroyed, transforming into a chaotic saddle (creating transient chaos).
