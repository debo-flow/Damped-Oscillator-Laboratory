"""
Milestone 17: Chaos Evidence & Classification
Unifies Lyapunov, Poincaré, Spectral, and Geometric diagnostics into a conservative classification.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ChaosEvidence:
    lyapunov_positive: bool
    poincare_complex: bool
    broadband_spectrum: bool
    fractal_dimension: bool
    transient_status: str
    crisis_candidate: bool
    intermittency_candidate: bool
    confidence_level: str
    classification: str

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

class ChaosClassifier:
    @staticmethod
    def classify(diagnostics: Dict[str, Any]) -> ChaosEvidence:
        """Evaluates multiple diagnostics to classify the dynamical regime conservatively."""
        
        # Extract individual diagnostic flags
        lle = diagnostics.get('lambda_max', 0.0)
        lle_converged = diagnostics.get('lyapunov_converged', False)
        lyap_pos = (lle > 1e-3) and lle_converged
        lyap_zero = abs(lle) <= 1e-3 and lle_converged
        
        poincare_pts = diagnostics.get('poincare_count', 0)
        poincare_complex = poincare_pts > 50  # Arbitrary threshold for complex scatter vs finite period
        
        d_ky = diagnostics.get('D_KY', 0.0)
        fractal_dim = (d_ky % 1 > 0.05) and (d_ky % 1 < 0.95) # Non-integer dimension
        
        transient = diagnostics.get('transient_chaos', False)
        intermittency = diagnostics.get('intermittency', False)
        crisis = diagnostics.get('crisis_detected', False)

        # Multi-Diagnostic Evaluation
        confidence = "low"
        classification = "numerically_uncertain"

        if not lle_converged:
            classification = "numerically_uncertain"
        elif transient:
            classification = "transient_chaos_candidate"
            confidence = "medium"
        elif intermittency:
            classification = "intermittency_candidate"
            confidence = "medium"
        elif lyap_pos and poincare_complex and fractal_dim:
            classification = "strongly_supported_chaos"
            confidence = "high"
        elif lyap_pos and (poincare_complex or fractal_dim):
            classification = "chaotic_candidate"
            confidence = "medium"
        elif lyap_zero and poincare_pts > 0 and poincare_pts <= 16:
            classification = "periodic_window" if diagnostics.get('in_chaotic_region') else "periodic"
            confidence = "high"
        elif lyap_zero and poincare_complex:
            classification = "quasiperiodic_candidate"
            confidence = "medium"
        elif lle < -1e-3:
            classification = "fixed_point_or_stable_sink"
            confidence = "high"

        return ChaosEvidence(
            lyapunov_positive=lyap_pos,
            poincare_complex=poincare_complex,
            broadband_spectrum=diagnostics.get('broadband_spectrum', False),
            fractal_dimension=fractal_dim,
            transient_status="transient_escape" if transient else "asymptotic",
            crisis_candidate=crisis,
            intermittency_candidate=intermittency,
            confidence_level=confidence,
            classification=classification
        )
