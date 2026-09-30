"""
Real-Time Deepfake Classifier & Artifact Detector Model Stub
Evaluates extracted DSP features (Phase incoherence, high frequency cutoff, centroid volatility)
and returns a synthetic risk score (0.0 to 1.0) with granular telemetry breakdown.
"""

import math
import numpy as np


class DeepfakeDetectorModel:
    """
    Lightweight Deepfake & Voice Conversion Artifact Classifier.
    """

    def __init__(self, high_risk_threshold: float = 0.70):
        self.high_risk_threshold = high_risk_threshold
        # Historical buffer to compute feature stability over frames
        self.centroid_history = []
        self.max_history = 10

    def reset(self):
        """Resets centroid history buffer."""
        self.centroid_history.clear()

    def predict(self, features: dict) -> dict:
        """
        Evaluates real-time audio frame metrics and computes synthetic probability score.
        """
        rms = features.get("rms_energy", 0.0)
        
        # If quiet silence, return clean baseline
        if rms < 0.005:
            return {
                "risk_score": 0.0,
                "risk_percentage": 0.0,
                "confidence": 1.0,
                "label": "SILENCE",
                "is_synthetic": False,
                "artifact_analysis": {
                    "phase_anomaly_score": 0.0,
                    "spectral_cutoff_score": 0.0,
                    "pitch_stability_score": 0.0
                }
            }

        phase_incoherence = features.get("phase_incoherence", 0.0)
        high_freq_ratio = features.get("high_freq_ratio", 0.0)
        centroid = features.get("spectral_centroid", 0.0)

        # Track centroid variance across recent frames
        if math.isfinite(centroid) and centroid > 0:
            self.centroid_history.append(centroid)
            if len(self.centroid_history) > self.max_history:
                self.centroid_history.pop(0)

        centroid_std = float(np.std(self.centroid_history)) if len(self.centroid_history) > 2 else 0.0

        # Artifact Score Heuristics:
        # 1. Phase Anomaly: Neural vocoders (HiFi-GAN, WaveGlow) exhibit phase incoherence variance > 1.2
        phase_anomaly_score = min(1.0, max(0.0, (phase_incoherence - 0.5) / 1.5))
        
        # 2. High-Frequency Spectral Cutoff: Synthetic voice conversion engines often cut off abruptly > 6.5kHz
        spectral_cutoff_score = min(1.0, max(0.0, (0.05 - high_freq_ratio) / 0.05)) if high_freq_ratio < 0.05 else 0.0

        # 3. Unnatural Pitch/Centroid Rigidity or Volatility
        pitch_stability_score = min(1.0, max(0.0, (500.0 - centroid_std) / 500.0)) if centroid_std < 50.0 else 0.0

        # Weighted combination of artifact scores
        raw_risk_score = (
            (phase_anomaly_score * 0.45) +
            (spectral_cutoff_score * 0.35) +
            (pitch_stability_score * 0.20)
        )

        # Scale and constrain risk score [0.0, 1.0]
        risk_score = round(float(np.clip(raw_risk_score, 0.02, 0.99)), 4)
        is_synthetic = risk_score >= self.high_risk_threshold
        
        label = "DEEPFAKE / SYNTHETIC" if is_synthetic else ("SUSPICIOUS" if risk_score > 0.45 else "AUTHENTIC HUMAN")

        return {
            "risk_score": risk_score,
            "risk_percentage": round(risk_score * 100, 1),
            "confidence": round(0.85 + (0.12 * abs(risk_score - 0.5)), 2),
            "label": label,
            "is_synthetic": is_synthetic,
            "artifact_analysis": {
                "phase_anomaly_score": round(float(phase_anomaly_score), 3),
                "spectral_cutoff_score": round(float(spectral_cutoff_score), 3),
                "pitch_stability_score": round(float(pitch_stability_score), 3)
            }
        }

