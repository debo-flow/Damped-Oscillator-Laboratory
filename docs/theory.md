## 19. Data-Driven System Identification & Reduced Order Modeling
Physics models are often derived first principles, but real-world complex systems frequently require extracting dynamics directly from observed trajectory data. 

### Parameter Estimation and Identifiability
Given an observed trajectory $\mathbf{x}_{obs}(t)$ and an assumed model structure $\dot{\mathbf{x}} = f(\mathbf{x}, \mathbf{p})$, parameters $\mathbf{p}$ are recovered by minimizing the residual sum of squares:
$$\min_{\mathbf{p}} \sum_i ||\mathbf{x}_{pred}(t_i, \mathbf{p}) - \mathbf{x}_{obs}(t_i)||^2$$
The **Fisher Information Matrix** (approximated as $H \approx J^T J$ where $J$ is the Jacobian of the residuals) quantifies identifiability. If the condition number of $H$ is immense, the parameters are *poorly identifiable*, meaning multiple different parameter sets yield indistinguishable trajectories.

### Sparse Equation Discovery (SINDy)
To discover the governing equations without assuming a model structure, we build a library matrix $\Theta(\mathbf{X})$ of candidate nonlinear functions (polynomials, sines, etc.). The dynamics are approximated as:
$$\dot{\mathbf{X}} = \Theta(\mathbf{X}) \Xi$$
We solve for $\Xi$ using **Sequential Thresholded Least Squares (STLSQ)**, forcing small coefficients to zero to isolate the sparsest (most physically meaningful) set of governing terms. *Warning: Numerical derivatives ($\dot{\mathbf{X}}$) are highly sensitive to observation noise.*

### Dynamic Mode Decomposition (DMD) & Koopman Operator
**DMD** extracts spatiotemporal coherent structures from data. By taking snapshot matrices $X$ and $Y$ (where $Y$ is one time-step ahead of $X$), DMD finds a finite-dimensional linear operator $\tilde{A}$ that best approximates $Y \approx A X$. 
**Extended DMD (EDMD)** approximates the infinite-dimensional **Koopman Operator** by "lifting" the state space into a higher-dimensional nonlinear observable dictionary $\Psi(\mathbf{X})$, mapping nonlinear dynamics into a globally linear framework.

### Proper Orthogonal Decomposition (POD)
**POD** compresses high-dimensional state spaces (e.g., $N$ coupled oscillators) into a Reduced-Order Model (ROM). Taking the Singular Value Decomposition (SVD) of the snapshot matrix $\mathbf{X} = U \Sigma V^T$, we truncate the basis to rank $r$, retaining the modes containing the highest fractional energy. The state is projected via $\mathbf{z} = U_r^T \mathbf{x}$.
