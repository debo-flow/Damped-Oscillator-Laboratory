"""
Milestone 19: Scientific Reproducibility
Captures software, hardware, and parameter configurations for exact provenance.
"""

import sys
import json
import platform
import datetime
import numpy as np
from typing import Dict, Any

class ReproducibilityTracker:
    @staticmethod
    def generate_manifest(experiment_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a provenance manifest containing environment metadata."""
        return {
            'experiment_name': experiment_name,
            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'environment': {
                'python_version': sys.version,
                'os': platform.platform(),
                'numpy_version': np.__version__
            },
            'configuration': config
        }

    @staticmethod
    def export_manifest(manifest: Dict, filepath: str):
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(manifest, f, indent=4)
        print(f"Reproducibility manifest exported to {filepath}")

