"""
Milestone 6: Forcing Module
Provides a modular interface for external driving forces on the oscillator.
"""

import numpy as np
from typing import Protocol

class ForcingFunction(Protocol):
    def __call__(self, t: float) -> float:
        """Returns the external force at time t."""
        ...

class ZeroForcing:
    def __call__(self, t: float) -> float:
        return 0.0

class SinusoidalForcing:
    def __init__(self, F0: float, omega: float):
        if F0 < 0:
            raise ValueError("Driving amplitude F0 must be non-negative.")
        if omega < 0:
            raise ValueError("Driving angular frequency omega must be non-negative.")
        self.F0 = F0
        self.omega = omega

    def __call__(self, t: float) -> float:
        return self.F0 * np.cos(self.omega * t)
