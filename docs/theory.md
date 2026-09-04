## 15. Full Lyapunov Spectrum and Attractor Geometry
While $\lambda_{\max}$ identifies sensitive dependence, the **Full Lyapunov Spectrum** ($\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$) provides a complete picture of phase-space stretching and contracting across all topological dimensions. 

### Tangent Space and QR Reorthonormalization
To compute the full spectrum, we track the evolution of an entire basis of orthogonal perturbation vectors, structured as a matrix $V$. The tangent space dynamics are governed by the Jacobian:
$$\dot{V} = J(\mathbf{x}, t) V$$
Because all vectors naturally align with the direction of fastest growth ($\lambda_1$), $V$ rapidly becomes ill-conditioned. To prevent this, we periodically decompose the matrix into an orthogonal basis $Q$ and an upper triangular scaling matrix $R$ using **QR Decomposition** ($V = QR$).
The spectrum is extracted by time-averaging the logarithms of the diagonal growth elements:
$$\lambda_i = \lim_{T \to \infty} \frac{1}{T} \sum_k \ln \vert{}R_{ii}^{(k)}\vert{}$$

For dissipative systems, phase-space volume contracts over time, mathematically forcing the sum of all exponents to be strictly negative ($\sum \lambda_i < 0$).

### The Kaplan–Yorke Dimension ($D_{KY}$)
Chaotic dissipative systems compress state space onto infinitely detailed structures called **Strange Attractors**. The Kaplan–Yorke conjecture links the continuous Lyapunov spectrum to the attractor's fractal geometry. Finding the largest index $j$ where the cumulative sum of exponents is still positive:
$$D_{KY} = j + \frac{\sum_{i=1}^j \lambda_i}{\vert{}\lambda_{j+1}\vert{}}$$
This provides a non-integer dimensional representation of the attractor's geometric complexity.

### Numerical Fractal Dimensions
Complementing Lyapunov calculations, purely geometric diagnostics verify attractor topology:
*   **Box-Counting Dimension ($D_{box}$):** Evaluates spatial occupancy by placing the attractor on a grid of size $\epsilon$ and counting occupied boxes $N(\epsilon)$. If scaling exists: $N(\epsilon) \propto \epsilon^{-D_{box}}$.
*   **Correlation Dimension ($D_2$):** Analyzes pairwise spatial probabilities, estimating the dimension from the correlation sum $C(r)$ across length scales $r$.
*Warning: Numerical estimation of $D_{box}$ and $D_2$ is highly sensitive to trajectory length, noise, and appropriate scale selection. A rigorous $R^2$ fit evaluation is mandatory before claiming fractal properties.*
