# Damped-Oscillator-Laboratory

## Project Description
A numerical simulation environment studying the physics of linear, nonlinear, and coupled harmonic oscillators. The engine bridges discrete stroboscopic chaos diagnostics, full Lyapunov spectrum generation, and rigorous adaptive bifurcation continuation to trace complete global dynamical maps.

## Features
*   **Continuation Engine:** Adaptive forward/backward pseudo-tracking to trace stable and unstable equilibrium branches continuously across parameter sweeps.
*   **Floquet & Monodromy Analysis:** Calculates Monodromy matrices over orbital periods to extract exact Floquet Multipliers, mathematically validating periodic orbit stabilities.
*   **Candidate Bifurcation Detection:** Automatically flags critical topological phase transitions including Saddle-Nodes ($Re(\mu) \to 0$), Hopf crossings ($Im(\mu) \neq 0$), Torus transitions ($\vert{}\rho\vert{} \to 1$), and Period-Doubling cascades ($\rho \to -1$).
*   **Basin of Attraction Mapping:** Automates 2D phase-space grid sampling to trace Multistability boundaries and group identical long-term geometric attractors.
*   **Global Overlays:** Superimposes Quantitative Chaos diagnostics (Largest Lyapunov Exponents, Kaplan-Yorke Dimensions) directly onto Bifurcation stability graphs for comprehensive regime mapping.
*   **Automated Testing:** `pytest` regression suite ensuring absolute root-finding residual limits ($< 10^{-6}$), exact Floquet-multiplier categorizations, and pitchfork eigenvalue stability reductions.

## Project Structure
```text
Damped-Oscillator-Laboratory/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── damped_oscillator.py
│   ├── damping_analysis.py
│   ├── analytical_solution.py
│   ├── validation_lab.py
│   ├── phase_space.py
│   ├── energy_analysis.py
│   ├── forcing.py
│   ├── resonance_analysis.py
│   ├── spectral_analysis.py
│   ├── coupled_oscillators.py
│   ├── nonlinear_oscillators.py
│   ├── van_der_pol.py
│   ├── chaos_analysis.py
│   ├── lyapunov_analysis.py
│   ├── attractor_analysis.py
│   ├── bifurcation_analysis.py
│   ├── continuation.py
│   ├── equilibrium_analysis.py
│   ├── periodic_orbit_analysis.py
│   └── branch_tracking.py
├── experiments/
│   ├── periodic_case.json
│   ├── complex_case.json
│   ├── lyapunov_scan.json
│   ├── attractor_dimension.json
│   ├── bifurcation_scan.json
│   └── multistability.json
├── tests/
│   ├── test_bifurcation_analysis.py
│   └── (all previous tests...)
├── docs/
│   └── theory.md
└── results/
