## 10. Coupled Oscillators and Normal Modes
When two harmonic oscillators are connected (e.g., via a coupling spring $k_c$), their equations of motion become inextricably linked. For two masses $m_1$ and $m_2$ grounded by springs $k_1$ and $k_2$:

$$m_1\ddot{x}_1 + b_1\dot{x}_1 + k_1x_1 + k_c(x_1-x_2) = 0$$
$$m_2\ddot{x}_2 + b_2\dot{x}_2 + k_2x_2 + k_c(x_2-x_1) = 0$$

### Matrix Formulation and State-Space
This system can be written elegantly in matrix form:
$$\mathbf{M}\ddot{\mathbf{x}} + \mathbf{C}\dot{\mathbf{x}} + \mathbf{K}\mathbf{x} = \mathbf{0}$$
Where $\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$, $\mathbf{M}$ is the mass matrix, $\mathbf{C}$ is the damping matrix, and $\mathbf{K}$ is the stiffness matrix.

### Normal Modes and Eigenfrequencies
For the undamped system ($\mathbf{C} = 0$), substituting an oscillatory solution $\mathbf{x}(t) = \mathbf{u} e^{i\omega t}$ yields the **Generalized Eigenvalue Problem**:
$$\mathbf{K}\mathbf{u} = \omega^2 \mathbf{M}\mathbf{u}$$
The resulting eigenvalues $\lambda_i$ give the **Normal Frequencies** ($\omega_i = \sqrt{\lambda_i}$). The corresponding eigenvectors $\mathbf{u}_i$ define the **Mode Shapes**. 

For identical oscillators ($m_1=m_2=m, k_1=k_2=k$):
1.  **Symmetric Mode:** $x_1 = x_2$. The coupling spring is not stretched. $\omega_1 = \sqrt{\frac{k}{m}}$.
2.  **Antisymmetric Mode:** $x_1 = -x_2$. The masses move in exact opposition. $\omega_2 = \sqrt{\frac{k + 2k_c}{m}}$.

Any arbitrary motion of the linear system is simply a superposition (linear combination) of these independent normal modes.

### Beating and Energy Exchange
If the coupling is very weak ($k_c \ll k$), the two normal frequencies are nearly identical. If excited asymmetrically (e.g., pulling only one mass), the system exhibits **Beating**. Energy slowly and completely transfers back and forth between the two oscillators at the beat frequency: $f_{beat} = \vert{}f_2 - f_1\vert{}$. Though subsystem energies fluctuate wildly, the total mechanical energy ($E_{tot} = K + U_g + U_c$) remains perfectly conserved in the undamped case.
